# Fetch Receipt Processor Challenge

## Docker

There is nothing extra needed to run this than what is included in this repository.
Navigate to the package and then begin.

```shell
$ docker build -t receipt_processor .
```
```shell
$ docker run -p 8000:8000 receipt_processor
```

If you would like to run the test cases within docker you can do the following:
```shell
$ docker run -p 8000:8000 receipt_processor sh -c "pytest tests/"
```


# Notes

### Python and Fastapi

I chose python simply because it's the language I have the most experience in and would be the easiest for me to showcase my abilities. Fastapi is by far and away my favorite framework to utilize within the python language and personally the best backend framework among what I deem the big 3 for python (Flask, Django, Fastapi). It doesn't try to do too much and gives you the option of utilizing additional features without forcing you into it, mainly focusing on just ensuring the api production experience is top notch and on par if not better than Flask.

I will note that I left the root route `"/"` in there even though it isn't defined in schema, I personally just prefer having something in the root route even if it's just text saying hey there is nothing here. Just to ensure that everything spun up correctly and the url just needs to be changed. Hopefully I won't be docked for this.

### Pydantic Models

Fastapi makes use of Pydantic for handling data models which I think is a great choice. One of the things that you will notice is the `Receipt` and `Item` models contain a lot of information for the simplicity that they are. Each field within the models contain an Annotation, this is a Pydantic feature that allows for adding extra information about a field; this information is actually extremely useful. The annotation on the fields are utilized in auto generated API docs. You can visit these at (http://127.0.0.1:8000/docs) when the server is running. It helps to provide detailed information in those docs as well as aiding validation. JSON tends to use the camelCase convention while python tends to use the snake_case convention for naming, Pydantic will utilize the alias annotation on the field in order to handle that validation and serialization. You'll also notice within the model definition the ineheratance of BaseModel, this is direct from pydantic to handle those built in features, as well as the value `populate_by_name=True`. That value setting to True allows the validation and serialization to occur on either the field defined in python or the alias annotation, so that way you can both create the object in Python by populating the fields (needed for test cases) or create the object from a json model (needed while running). One additional feature that may be noticed on the field annotations is the pattern, this regex pattern is actually validated when creating the object from json and will error if the passed in value for that field does not match that pattern.

#### Out Models

Another thing to note about Pydantic and something you'll notice within the code is the 'Out' models located within the receipts route. These 'Out' models are defined in order to aid in the api docs as a response example.

### Exception Handler

One of the things you'll notice in the main file that defines the app and the api routes is an override to an exception handler. This override is to handle conforming to the provided schema so when a validation exception occurs (something predefined within Pydantic when it converts from json to Python mdoel) it will output a 400 HTTP error instead of a 422 HTTP error, along with altering the text that is output based on the provided schema as well. I do think a 422 HTTP error would be the better option if I had the oportunity to change that, but I wanted to make sure that the schema given is the one that the system provides. 

I will also note that because of the way this is handled as on override and the way Pydantic defaults to a 422 error, the auto generated api docs will show a 422 error as an option (I could not figure out how to remove that from the docs) even though the server itself will output a 400 on a validation exception. 

***Note:*** A 422 HTTP error from validation will not occur, there is a test that confirms this

### Testing

I have two types of testing provided within the test suite; unit tests and end to end tests utilizing the api. 

The unit tests themselves are self explanatory, I opt for descriptive names in tests so that way it's easy to comprehend, as well as utilizing the function name under test, the default case is a test for a successful expected result. Alternative cases for a function are named appropriately. The unit tests themselves do not need to handle testing for type or validation checks because of the way that Pydantic handles the json to object conversion, those things will fail out before these functions are even called, so we can safely operate under the assumption that types and patterns are valid at the point of input.

For the end to end api tests I utilize a pytest fixture which can be seen in the test function `test_get_receipt_points(receipt_id: str)`. The `receipt_id` value there is an input from a pytest fixture above `receipt_id() -> str`, the output from that function is utilized as the input to the actual test. The reason this is done is to ensure that there is a receipt that has been processed in memory (since we aren't using any database) for the test to be able to operate with.

#### Future Dated Receipt

One of the things I noticed within the instructions is that there is no mention of what to do in the event that a receipt is given with a future date. I came across this mainly from trying to test unexpected circumstances where valid typing and patterns are given, but the input is still unexpected. I went with the assumption that this is a malformed receipt and that it should be rejected with status code 400, including the standard schema text response, but because no direct schema was defined for this I added the text that it contains a future date.

## Overall

I will say that I thoroughly enjoyed this programming challenge. It was a great way to showcase coding ability without feeling the pressure, nervousness and anxiety of a timed in person session. I also really like how y'all put in those gotchas for people who try and create all of this via some LLM like chatgpt or something, I thought that was pretty clever and funny. Additionally I will say that there are probably some test cases I did not check for, initially think about, etc. There is always more work that can be done to improve things, and although striving for perfection is always great, at some point work has to be shipped and as engineers we have to live with the knowledge that we can always continue to add improvements after the fact. I look forward to being able to chat with y'all about this at some point in the future.
