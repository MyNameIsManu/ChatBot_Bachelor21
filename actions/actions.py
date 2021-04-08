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
##from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.forms import FormAction

class ActionCompanySearch(Action):

    def name(self) -> Text:
        return "action_company_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        company = tracker.get_slot("company")
        address = "Gleiwitzer Str. 555, 90475 Nürnberg"
        dispatcher.utter_message(text="Die Adresse von {}: {}".format(company, address))

        return [SlotSet("address", address)]

class LocationForm(FormAction):
    """Custom form action to fill all slots required to find specific type
    of healthcare facilities in a certain city or zip code."""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "company"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["company", "location"]

    def slot_mappings(self) -> Dict[Text, Any]:
        return {"company": self.from_entity(entity="company",
                                                  intent=["inform",
                                                          "search_company"]),
                "location": self.from_entity(entity="location",
                                             intent=["inform",
                                                     "search_company"])}

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) -> List[Dict]:
        """Once required slots are filled, print buttons for found facilities"""

        location = tracker.get_slot('location')
        company = tracker.get_slot('company')

        results = _find_company(location, company)
        button_name = _resolve_name(COMPANIES, company)
        if len(results) == 0:
            dispatcher.utter_message(
                "Sorry, we could not find a {} in {}.".format(button_name,
                                                              location.title()))
            return []


        buttons = []
        # limit number of results to 3 for clear presentation purposes
        for r in results[:3]:
            if company == COMPANIES["Siemens"]["resource"]:
                company_id = r.get("id")
                name = r["name"]
            elif company == COMPANIES["Datev"]["resource"]:
                company_id = r["id"]
                name = r["name"]
            else:
                company_id = r["id"]
                name = r["name"]

            payload = "/inform{\"company_id\":\"" + company_id + "\"}"
            buttons.append(
                {"title": "{}".format(name.title()), "payload": payload})

        if len(buttons) == 1:
            message = "Here is a {} near you:".format(button_name)
        else:
            if button_name == "test":
                button_name = "tests"
            message = "Here are {} {}s near you:".format(len(buttons),
                                                         button_name)

        # TODO: update rasa core version for configurable `button_type`
        dispatcher.utter_button_message(message, buttons)

        return []