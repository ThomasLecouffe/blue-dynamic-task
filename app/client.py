from os.path import altsep

import grpc
from google.protobuf.timestamp_pb2 import Timestamp

from proto import db_pb2, db_pb2_grpc


class DatabaseClient:
    def __init__(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = db_pb2_grpc.DatabaseServiceStub(self.channel)

    def GetBox(self, id: int):
        request = db_pb2.GetBoxRequest(id=id)
        response = self.stub.GetBox(request)
        return response

    def GetBoxes(self):
        request = db_pb2.GetAllBoxesRequest()
        response = self.stub.GetBoxes(request)
        return response

    def CreateBox(self, box: dict):
        request = db_pb2.CreateBoxRequest(box=box)
        response = self.stub.CreateBox(request)
        return response

    def UpdateBox(self, box: dict):
        request = db_pb2.UpdateBoxRequest(box=box)
        response = self.stub.UpdateBox(request)
        return response

    def DeleteBox(self, id: int):
        request = db_pb2.DeleteBoxRequest(id=id)
        response = self.stub.DeleteBox(request)
        return response

    def GetBoxesInCategory(self, category: str):
        request = db_pb2.GetBoxesInCategoryRequest(category=category)
        response = self.stub.GetBoxesInCategory(request)
        return response

    def GetBoxesInTimeRange(self, start_time, end_time):
        request = db_pb2.GetBoxesInTimeRangeRequest(start_time=start_time, end_time=end_time)
        response = self.stub.GetBoxesInTimeRange(request)
        return response


if __name__ == "__main__":
    """The only purpose of these lines is to test
    all the different API endpoints
    """
    client = DatabaseClient()

    timestamp = Timestamp()
    timestamp.GetCurrentTime()

    box = {
        "name": "test_name",
        "id": 1,
        "price": 15,
        "description": "lorem ipsum",
        "category": "category_1",
        "quantity": 3,
        "created_at": timestamp,
    }

    print("test create one box, should display one box")
    print(client.CreateBox(box))
    print(client.GetBox(id=1))

    timestamp.GetCurrentTime()
    box2 = {
        "name": "box2",
        "id": 2,
        "price": 20,
        "description": "lorem ipsum 2",
        "category": "category_1",
        "quantity": 2,
        "created_at": timestamp,
    }

    print(client.CreateBox(box2))
    print("test get all boxes, should display two objects")
    print(client.GetBoxes())

    box2["name"] = "new box name"

    print("update box, the box should have name: 'new box name'")
    print(client.UpdateBox(box2))
    print(client.GetBox(id=2))

    new_category_box = {
        "name": "new_category_box",
        "id": 3,
        "price": 68,
        "description": "lorem ipsum 2",
        "category": "category_2",
        "quantity": 18,
        "created_at": timestamp,
    }

    print(client.CreateBox(new_category_box))

    print("get category 1 (two boxes)")
    print(client.GetBoxesInCategory(category="category_1"))
    print("get category 2 (one box)")
    print(client.GetBoxesInCategory(category="category_2"))

    # Test delete function
    print(client.DeleteBox(id=1))
    print("test the delete function, should delete id=1 item (two items remaining)")
    print(client.GetBoxes())

    # Clean the database
    print(client.DeleteBox(id=2))
    print(client.DeleteBox(id=3))
    print(client.GetBoxes())

    # Test range time
    print("test range time")
    box2["created_at"] = Timestamp(seconds=20)
    print(client.CreateBox(box2))

    box2["created_at"] = Timestamp(seconds=45)
    box2["id"] = 3
    print(client.CreateBox(box2))

    start_time = Timestamp(seconds=15)
    end_time = Timestamp(seconds=35)
    print("between 15 and 35 seconds, should retrieve one box")
    print(client.GetBoxesInTimeRange(start_time, end_time))

    end_time = Timestamp(seconds=60)
    print("between 15 and 60 seconds, should retrieve two boxes")
    print(client.GetBoxesInTimeRange(start_time, end_time))

    client.DeleteBox(id=2)
    client.DeleteBox(id=3)

    print("get boxes (should be empty)")
    print(client.GetBoxes())
