module Types.HealthCheck where

import Data.Aeson
import GHC.Generics

data ResponseTime = Microseconds Int | Timeout
  deriving (Eq, Show, Generic)

instance ToJSON ResponseTime where
  toEncoding = genericToEncoding defaultOptions

instance FromJSON ResponseTime

doubleToMicroseconds :: Double -> ResponseTime
doubleToMicroseconds = Microseconds . round . (* 1000000)

data HealthCheckResponse
  = HealthCheckResponse
      { statusCode :: Int,
        -- elapsed time in microseconds
        responseTime :: ResponseTime
      }
  | NoResponse
  deriving (Show, Generic)

instance ToJSON HealthCheckResponse where
  toEncoding = genericToEncoding defaultOptions

instance FromJSON HealthCheckResponse
