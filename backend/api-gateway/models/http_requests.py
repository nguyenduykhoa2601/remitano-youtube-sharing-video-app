import requests
import json


class HTTPRequest:
    def __init__(self, url, method):
        self.url = url
        self.method = method.upper()  # Ensure the method is in uppercase
        # Validate the method
        valid_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
        if self.method not in valid_methods:
            raise ValueError(
                f"Invalid method. Supported methods are: {', '.join(valid_methods)}"
            )

    def send_request(self, data=None, headers=None):
        """
        Send the HTTP request based on the initialized parameters.

        :param data: Optional data to include in the request body.
        :param headers: Optional headers to include in the request.
        :return: Response data as JSON if possible, otherwise raw text.
        """
        try:
            # Map the HTTP method to the corresponding requests function
            method_function = getattr(requests, self.method.lower())
            # Send the request
            response = method_function(
                self.url, json=data, headers=headers, timeout=600
            )
            response.raise_for_status()  # Raise an error for bad status codes

            # Attempt to parse the response as JSON
            try:
                return response.json()
            except json.JSONDecodeError:
                # Handle non-JSON responses
                print("Response is not valid JSON:", response.text)
                return {
                    "error": "Invalid response format",
                    "status_code": response.status_code,
                    "content": response.text,
                }
        except requests.exceptions.RequestException as e:
            # Log the exception details
            print(f"HTTP Request failed: {str(e)}")
            return {
                "error": str(e),
                "status_code": response.status_code if 'response' in locals() else 500,
            }
