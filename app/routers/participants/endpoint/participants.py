from fastapi import APIRouter, Form, File, UploadFile
from routers.participants.schemas import participants
from routers.events.models.models import Event
from routers.participants.models.models import Participant
from utils.database import Database
from passlib.context import CryptContext
from routers.participants.repo import crud



# APIRouter creates path operations for staffs module
router = APIRouter(
    prefix="/participant",
    tags=["Participant"],
    responses={404: {"description": "Not found"}},
)




database = Database()
engine = database.get_db_connection()
session = database.get_db_session(engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



# @router.get("/read_image/{event_id}")
# async def read_flyer(event_id: int):
#     event_data = session.query(Event).filter(Event.id == event_id).first()
#     db_flyer_name = f'app/flyers/{event_data.flyer}'
#     return FileResponse(db_flyer_name)



#PARTICIPANT CRUD ENDPOINT

@router.post("/add", response_description="Participant data added into the database")
async def create_participants(participantRequest: participants.ParticipantRequest):

    return await crud.add_participants(participantRequest)





@router.get("/all")
async def all_Participant():

    return await crud.all_Participant()





@router.get("/id/{id}")
async def get_Participant_By_Id(id: int):
    
    return await crud.get_Participant_By_Id(id)
    








@router.put("/update")
async def updateParticipant(updateParticipant: participants.UpdateParticipant):
    
    return await crud.updateParticipant(updateParticipant)










@router.get("/event_id/{event_id}")
async def get_Participants_By_Event_ID(event_id: int):
    
    return await crud.get_Participants_By_Event_ID(event_id)














# @router.get("/phone_number_email/{phone_number_email}")
# async def phone_number_email(phone_number_email: str):
    
#     return await crud.phone_number_email(phone_number_email)




    





# @router.get("/attend_program_by/{how_to_join}")
# async def get_Participant_By_how_to_join(how_to_join: str):
    
#     return await crud.get_Participant_By_how_to_join(how_to_join)








# @router.delete("/delete/{id}")
# async def deleteParticipant(id: str):
    
#     return await crud.deleteParticipant(id)







# @router.get("/participant_event/{id}")
# async def show_participant_event_all(id: int):
    
#     return await crud.show_participant_event_all(id)









# @router.get("/countParticipant")
# async def count_all_Participant():
    
#     return await crud.count_all_Participant()





# @router.get("/countParticipantConfirm")
# async def count_all_Participant_Confirm():
    
#     return await crud.count_all_Participant_Confirm()





# @router.get("/countParticipantNotConfirm")
# async def count_all_Participant_Not_Confirm():
    
#     return await crud.count_all_Participant_Not_Confirm()


