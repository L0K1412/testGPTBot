from typing import Optional

from pydantic import BaseModel, Field


class TokenName(BaseModel):
    token_name: Optional[str] = Field(
        description="token name, either in full name or short form"
    )


class GetTokenWebsite(object):
    name = "token_website"
    description = "Get the token website or social channels."

    @property
    def examples(self):
        return ["What is Pendle's website", "What are Pendle's social channels?"]

    @property
    def entities(self):
        # Define structure of entities
        return TokenName(token_name=None)

    @staticmethod
    def fulfill(**kwargs):
        token_name = kwargs["token_name"]
        return "Here is the link to {} website: api.get_token_website".format(
            token_name
        )

    def promt(self):
        template = (
            "Name: {} \n" "Description: {} \n" "Examples: {} \n" "Entities: {} \n\n"
        )
        return template.format(
            self.name, self.description, self.examples, self.entities
        )


class GetTokenPrice(object):
    name = "token_price"
    description = "Get the price for a token"

    @property
    def examples(self):
        return ["Price ETH", "ETH price", "What is the price of ETH"]

    @property
    def entities(self):
        # Define structure of entities
        return TokenName(token_name=None)

    @staticmethod
    def fulfill(**kwargs):
        token_name = kwargs["token_name"]
        return "Here is the price of {}: api.get_token_price".format(token_name)

    def promt(self):
        template = (
            "Name: {} \n" "Description: {} \n" "Examples: {} \n" "Entities: {} \n\n"
        )
        return template.format(
            self.name, self.description, self.examples, self.entities
        )


class GetTokenPriceChanges(object):
    name = "token_price_change"
    description = "Get the price for a token"

    @property
    def examples(self):
        return ["Price ETH changes", "price ETH changes 24h"]

    @property
    def entities(self):
        # Define structure of entities
        class PriceChangesEntities(BaseModel):
            token_name: Optional[str] = Field(
                description="token name, either in full name or short form"
            )
            duration: Optional[str] = Field(description="duration in hours")

        return PriceChangesEntities(
            token_name="Token name in short form", duration="time duration in hour unit"
        )

    @staticmethod
    def fulfill(**kwargs):
        print(kwargs)
        token_name = kwargs["token_name"]
        duration = kwargs["duration"]
        return "Here is the price changes of {} in last {}: api.get_token_price_changes".format(
            token_name, duration
        )

    def promt(self):
        template = (
            "Name: {} \n" "Description: {} \n" "Examples: {} \n" "Entities: {} \n\n"
        )
        return template.format(
            self.name, self.description, self.examples, self.entities
        )
