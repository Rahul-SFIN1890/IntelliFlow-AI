from services.sql_service import SQLService

service = SQLService()

response = service.execute(

    "Compare Rahul salary with bonus"

)

print("\nANSWER\n")

print(response["answer"])