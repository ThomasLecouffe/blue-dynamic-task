import logging
from concurrent import futures

import grpc
from google.protobuf.timestamp_pb2 import Timestamp
from pymongo import MongoClient

from proto import db_pb2, db_pb2_grpc


class DatabaseService(db_pb2_grpc.DatabaseService):
    @staticmethod
    def get_mongo_box_collection():
        client = MongoClient("mongodb", 27017)
        db = client["database-service"]
        box_collection = db.box
        return box_collection

    @staticmethod
    def get_box_data(box: dict) -> dict:
        if not box:
            return {}
        return {
            "name": box.get("name"),
            "id": box.get("id"),
            "price": box.get("price"),
            "description": box.get("description"),
            "category": box.get("category"),
            "quantity": box.get("quantity"),
            "created_at": Timestamp(seconds=box.get("created_at"), nanos=0),
        }

    def get_box_response_data(self, box: dict, status: db_pb2.RequestStatus) -> dict:
        return {
            "box": self.get_box_data(box),
            "status": status,
        }

    def get_boxes_response_data(self, boxes: list, status: db_pb2.RequestStatus) -> dict:
        return {
            "box": [self.get_box_data(box) for box in boxes],
            "status": status,
        }

    def get_boxes_response(self, query: dict):
        status = db_pb2.OK
        box_collection = self.get_mongo_box_collection()
        boxes = box_collection.find(query)

        data = self.get_boxes_response_data(boxes, status)
        return db_pb2.GetBoxesResponse(**data)

    def GetBox(self, request, context):
        status = db_pb2.OK
        box_collection = self.get_mongo_box_collection()
        box = box_collection.find_one({"id": request.id})

        if not box:
            status = db_pb2.ERROR

        data = self.get_box_response_data(box, status)
        return db_pb2.GetBoxResponse(**data)

    def GetBoxes(self, request, context):
        return self.get_boxes_response(query={})

    def CreateBox(self, request, context):
        status = db_pb2.OK
        box_collection = self.get_mongo_box_collection()

        data_to_insert = {
            "name": request.box.name,
            "id": request.box.id,
            "price": request.box.price,
            "description": request.box.description,
            "category": request.box.category,
            "quantity": request.box.quantity,
            "created_at": request.box.created_at.seconds,
        }

        box_collection.insert_one(data_to_insert)

        data = {"status": status}
        return db_pb2.CreateBoxResponse(**data)

    def UpdateBox(self, request, context):
        status = db_pb2.OK
        box_collection = self.get_mongo_box_collection()

        data_to_update = {
            "id": request.box.id,
            "name": request.box.name,
            "price": request.box.price,
            "description": request.box.description,
            "category": request.box.category,
            "quantity": request.box.quantity,
            "created_at": request.box.created_at.seconds,
        }

        box_collection.replace_one({"id": request.box.id}, data_to_update)

        data = {"status": status}
        return db_pb2.UpdateBoxResponse(**data)

    def DeleteBox(self, request, context):
        status = db_pb2.OK
        box_collection = self.get_mongo_box_collection()

        box_collection.delete_one({"id": request.id})

        data = {"status": status}
        return db_pb2.DeleteBoxResponse(**data)

    def GetBoxesInCategory(self, request, context):
        return self.get_boxes_response(query={"category": request.category})

    def GetBoxesInTimeRange(self, request, context):
        query = {
            "created_at": {
                "$gt": request.start_time.seconds,
                "$lt": request.end_time.seconds,
            }
        }
        return self.get_boxes_response(query=query)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    db_pb2_grpc.add_DatabaseServiceServicer_to_server(DatabaseService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    print("running the gRPC server")
    logging.basicConfig()
    serve()
