from fastapi import status, Form
from routers.participants.schemas import participants
from models.models import Participant, ParticipantFields, Event
from utils.database import Database
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from mail import sendmail
from fastapi.responses import FileResponse
import json




database = Database()
engine = database.get_db_connection()
session = database.get_db_session(engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


IMAGEDIR = "app/flyers"




async def read_flyer(event_id: int):
    event_data = session.query(Event).filter(Event.id == event_id).first()
    db_flyer_name = f'app/flyers/{event_data.flyer}'
    return FileResponse(db_flyer_name)



async def add_participants(participantRequest: participants.ParticipantRequest):

    # email_query = session.query(Participant).filter(
    #     Participant.email == participantRequest.email).first()
    
    # phone_query = session.query(Participant).filter(
    #     Participant.phone_number == participantRequest.phone_number).first()


    # contact_query = session.query(Participant).filter(
    #     Participant.contact == participantRequest.contact).first()


    # if email_query or phone_query or contact_query:
    #     raise HTTPException(status_code=status.HTTP_303_SEE_OTHER,
    #        detail=f"Participant with email or phone number already exists")


    new_participant = Participant()
    new_participant.form_values = json.dumps(participantRequest.form_values)
    new_participant.event_id = participantRequest.event_id
    new_participant.status = 0
    
    session.add(new_participant)
    session.flush()
    session.refresh(new_participant, attribute_names=['id'])

    #event_data = session.query(Event).filter(Event.id == participantRequest.event_id).first()
    #read_flyer_image = read_flyer(participantRequest.event_id)
    #db_flyer_name = f'app/flyers/{event_data.flyer}'

    #await sendmail.sendEmailToNewParticipant([new_participant.email], new_participant, read_flyer_image)
    session.commit()
    session.close()
    return new_participant






async def all_Participant():
    data = session.query(Participant).all()
    return data






async def get_Participant_By_Id(id: int):
    data = session.query(Participant).filter(Participant.id == id).all()
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Participant with the id (" + str(id) + ") is not found")
    return data
    









async def updateParticipant(updateParticipant: participants.UpdateParticipant):
    participant_id = updateParticipant.id
    is_Participant_update = session.query(Participant).filter(Participant.id == participant_id).update({
            Participant.name: updateParticipant.name,
            Participant.phone_number: updateParticipant.phone_number,
            Participant.gender: updateParticipant.gender,
            Participant.email: updateParticipant.email,
            Participant.organization: updateParticipant.organization,
            Participant.how_to_join: updateParticipant.how_to_join,
            Participant.registration_time: updateParticipant.registration_time,
            Participant.location: updateParticipant.location,
            Participant.event_id: updateParticipant.event_id,
            Participant.status: 1
        }, synchronize_session=False)
    session.flush()
    session.commit()
    if not is_Participant_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Participant with the id (" + str(participant_id) + ") is not found")

    data = session.query(Participant).filter(Participant.id == participant_id).one()
    return data











async def phone_number_email(phone_number_email: str):
    if "@" in phone_number_email:
        participant = session.query(Participant).filter(
            Participant.email == phone_number_email).first()
    else:
        participant = session.query(Participant).filter(
            Participant.phone_number == phone_number_email).first()
    return participant





    






async def get_Participant_By_how_to_join(how_to_join: str):
    data = session.query(Participant).filter(
            Participant.how_to_join == how_to_join).all()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attend by (" + str(how_to_join) + ") is not available")
    elif how_to_join == "virtual":
            data = session.query(Participant).filter(Participant.how_to_join == how_to_join).all()
    elif how_to_join == "onsite":
            data = session.query(Participant).filter(Participant.how_to_join == how_to_join).all()
    return data









async def deleteParticipant(id: str):
    db_data = session.query(Participant).filter(Participant.id == id).update({
            Participant.status: 0
            }, synchronize_session=False)
    session.flush()
    session.commit()
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Participant with the id (" + str(id) + ") is not available")

    data = session.query(Participant).filter(Participant.id == id).one()
    return data








async def show_participant_event_all(id: int):
    data = session.query(Participant).filter(
            Participant.event_id == Event.id).filter(Event.id == id).all()
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Participant with the id {id} is not available")
    return data









async def count_all_Participant():
    data = session.query(Participant).count()
    return data






async def count_all_Participant_Confirm():
    data = session.query(Participant).filter(Participant.status == 1).count()
    return data







async def count_all_Participant_Not_Confirm():
    data = session.query(Participant).filter(Participant.status == 0).count()
    return data


