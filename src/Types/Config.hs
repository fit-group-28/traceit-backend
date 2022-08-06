module Types.Config where

data Config = Config
  { port :: Int,
    host :: String
  }
  deriving (Show, Eq)