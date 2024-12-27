import json
import datetime
import time

def validate(slots):
    # List of valid cities for location validation
    valid_cities = ['mumbai', 'delhi', 'banglore', 'hyderabad']
    
    # Validate Location slot
    if not slots['Location']:
        print("Location slot is empty.")
        return {
            'isValid': False,
            'violatedSlot': 'Location'
        }
    
    # Safely access the value and call lower()
    if slots['Location']['value']['originalValue'].lower() not in valid_cities:
        print("Invalid location")
        return {
            'isValid': False,
            'violatedSlot': 'Location',
            'message': 'We currently  support only {} as a valid destination.?'.format(", ".join(valid_cities))
        }
    
    # Validate CheckInDate slot
    if not slots['DateIn']:
        print("CheckInDate slot is empty.")
        return {
            'isValid': False,
            'violatedSlot': 'DateIn'
        }
    
    # Validate Duration (Nights or Duration) slot
    if not slots['Duration']:
        print("Duration or Nights slot is empty.")
        return {
            'isValid': False,
            'violatedSlot': 'Duration'
        }
    
    # Validate Roomtype slot
    if not slots['Roomtype']:
        print("Roomtype slot is empty.")
        return {
            'isValid': False,
            'violatedSlot': 'Roomtype'
        }
    
    return {'isValid': True}

def lambda_handler(event, context):
    try:
        # Extract slots and intent from the event
        slots = event['sessionState']['intent']['slots']
        intent = event['sessionState']['intent']['name']
        print(event['invocationSource'])
        print(slots)
        print(intent)
        
        validation_result = validate(slots)
        
        if event['invocationSource'] == 'DialogCodeHook':
            # If validation fails, elicit the violated slot
            if not validation_result['isValid']:
                if 'message' in validation_result:
                    response = {
                        "sessionState": {
                            "dialogAction": {
                                'slotToElicit': validation_result['violatedSlot'],
                                "type": "ElicitSlot"
                            },
                            "intent": {
                                'name': intent,
                                'slots': slots
                            }
                        },
                        "messages": [
                            {
                                "contentType": "PlainText",
                                "content": validation_result['message']
                            }
                        ]
                    }
                else:
                    response = {
                        "sessionState": {
                            "dialogAction": {
                                'slotToElicit': validation_result['violatedSlot'],
                                "type": "ElicitSlot"
                            },
                            "intent": {
                                'name': intent,
                                'slots': slots
                            }
                        }
                    }
                return response
            
            # If validation is successful, delegate the next step
            else:
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "type": "Delegate"
                        },
                        "intent": {
                            'name': intent,
                            'slots': slots
                        }
                    }
                }
                return response
        
        if event['invocationSource'] == 'FulfillmentCodeHook':
            
            # Return the fulfillment response
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Close"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots,
                        'state': 'Fulfilled'
                    }
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": "Thanks, I have placed your reservation"
                    }
                ]
            }
            return response
    
    except Exception as e:
        print(f"Error processing the request: {str(e)}")
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    'name': "Error",
                    'slots': {},
                    'state': 'Fulfilled'
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "There was an error processing your request. Please try again later."
                }
            ]
        }
