# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionCompanySearch(Action):

    def name(self) -> Text:
        return "action_company_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        company = tracker.get_slot("company")
        address = "Gleiwitzer Str. 555, 90475 Nürnberg"
        dispatcher.utter_message(text="Die Adresse von {}:{}".format(company, address))

        return [SlotSet("address", address)]
