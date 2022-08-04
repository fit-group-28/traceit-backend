{-# LANGUAGE OverloadedStrings #-}

module HealthCheck where

import Control.Concurrent
import Control.Concurrent.STM
import Control.Monad.Except
import Data.Aeson
import Data.Foldable
import Data.Maybe
import GHC.Generics
import Network.HTTP.Simple
import Servant
import System.TimeIt
import Types.Config
import Types.HealthCheck

data Health = Health
  { helloWorld :: HealthCheckResponse,
    healthCheck :: HealthCheckResponse
  }
  deriving (Show, Generic)

instance ToJSON Health where
  toEncoding = genericToEncoding defaultOptions

instance FromJSON Health

toCheck :: [String]
toCheck = ["/hello"]

handleHealthCheck :: Config -> Handler Health
handleHealthCheck cfg = do
  (elapsedTime, responses) <- liftIO $ timeItT $ do
    responsesList <- newTVarIO []
    traverse_ (forkIO . checkEndpoint responsesList (host cfg) (port cfg)) toCheck
    atomically $ do
      queryResponses <- readTVar responsesList
      check $ length queryResponses == length toCheck
      pure queryResponses

  pure $ constructHealth elapsedTime responses
  where
    checkEndpoint :: TVar [(String, HealthCheckResponse)] -> String -> Int -> String -> IO ()
    checkEndpoint responsesList host port endpoint = do
      (elapsedTime, status) <-
        timeItT $
          fmap getResponseStatusCode $
            httpNoBody . setRequestPort port =<< parseRequest (host ++ endpoint)

      atomically $
        modifyTVar'
          responsesList
          ((endpoint, HealthCheckResponse status $ doubleToMicroseconds elapsedTime) :)

    constructHealth :: Double -> [(String, HealthCheckResponse)] -> Health
    constructHealth elapsedTime responses =
      let helloResponse = fromMaybe NoResponse $ lookup "/hello" responses
       in Health
            { helloWorld = helloResponse,
              healthCheck = HealthCheckResponse 200 $ doubleToMicroseconds elapsedTime
            }
