{-# LANGUAGE OverloadedStrings #-}

module HelloWorld (handleHello, Hello (..)) where

import Data.Aeson
import Data.Text qualified as T
import GHC.Generics
import Servant

newtype Hello = Hello {payload :: T.Text}
  deriving (Show, Generic)

instance ToJSON Hello where
  toEncoding = genericToEncoding defaultOptions

instance FromJSON Hello

handleHello :: Handler Hello
handleHello = pure $ Hello {payload = "Hello, world!"}