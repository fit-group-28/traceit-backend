{-# LANGUAGE DataKinds #-}
{-# LANGUAGE OverloadedStrings #-}

module Main where

import HealthCheck
import HelloWorld
import Network.Wai.Handler.Warp
import Network.Wai.Middleware.Cors
import Network.Wai.Middleware.RequestLogger
import Servant
import Types.Config

defaultConfig :: Config
defaultConfig =
  Config
    { port = 8080,
      host = "http://localhost"
    }

-- todo: make the host actually depend on the item in the host field
-- make the host type not a string, but some sort of parsed type from stdin args
-- logically couple cmdline args with host type
main :: IO ()
main = do
  run (port defaultConfig) $ (simpleCors . logStdoutDev) $ servApp defaultConfig

servApp :: Config -> Application
servApp = serve (Proxy :: Proxy TraceItAPI) . server1

type TraceItAPI =
  "health" :> Get '[JSON] Health
    :<|> "hello" :> Get '[JSON] Hello

server1 :: Config -> ServerT TraceItAPI Handler
server1 config =
  handleHealthCheck config
    :<|> handleHello
