from fastapi import APIRouter, status, Depends
from routers.admin.schemas import admin
from models.models import Admin
from utils.database import Database
from auth import authentication
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from mail.sendmail import sendemailtonewusers
from utils.config import settings
from datetime import timedelta





database = Database()
engine = database.get_db_connection()
session = database.get_db_session(engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")






async def admin_authentication(form_data: OAuth2PasswordRequestForm = Depends()):
    
    data=session.query(Admin).filter(Admin.email==form_data.username).first()

    if data and pwd_context.verify(form_data.password, data.password):
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = authentication.create_access_token(data={"email": data.email}, expires_delta=access_token_expires)

        db_data = {
            "access_token":access_token,
            "token_type": "bearer",
            "email": form_data.username,
            "usertype": data.usertype,
            "event_id": data.event_id
        }

        return db_data


    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                        detail="Invalid login credential"                   
    )












async def create_admin(adminRequest: admin.AdminRequest):

    db_query = session.query(Admin).filter(Admin.email == adminRequest.email).filter(
        Admin.contact == adminRequest.contact).first()
 
    if db_query is not None:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER,
           detail="Admin or User with email or phone number (" + \
        str(adminRequest.email) + ") already exists")
    
    new_admin = Admin()
    new_admin.name = adminRequest.name
    new_admin.email = adminRequest.email
    new_admin.contact = adminRequest.contact
    new_admin.usertype = adminRequest.usertype
    new_admin.event_id = adminRequest.event_id
    new_admin.password = pwd_context.hash("password")
    new_admin.reset_password_token = authentication.generate_reset_password_token()
    new_admin.status = "Active"
    session.add(new_admin)
    session.flush()
    session.refresh(new_admin, attribute_names=['id'])
    #await sendemailtonewusers([adminRequest.email], new_admin)
    session.commit()
    session.close()
    return new_admin













async def get_all_admin():
    data = session.query(Admin).filter(Admin.status == "Active").all()
    return data







async def getAdminById(id: str):
    data = session.query(Admin).filter(Admin.id == id).all()
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Admin or User with the id {id} is not found")
    return data








async def updateAdmin(updateAdmin: admin.UpdateAdmin):
    adminID = updateAdmin.id
    is_adminID_update = session.query(Admin).filter(Admin.id == adminID).update({
            Admin.name: updateAdmin.name,
            Admin.contact: updateAdmin.contact,
            Admin.email: updateAdmin.email,
            Admin.usertype: updateAdmin.usertype,
            Admin.event_id: updateAdmin.event_id
        }, synchronize_session=False)
    session.flush()
    session.commit()
    if not is_adminID_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin or User with the id (" + str(adminID) + ") is not found")

    data = session.query(Admin).filter(Admin.id == adminID).one()
    return data










async def getAdminByEmail(email: str):
    data = session.query(Admin).filter(Admin.email == email).all()
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Admin or User with the email {email} is not found")
    return data



















async def deleteAdmin(id: str):
    db_data = session.query(Admin).filter(Admin.id == id).update({
            Admin.status: "InActive"
            }, synchronize_session=False)
    session.flush()
    session.commit()
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin or User with the id {id} is not found")

    data = session.query(Admin).filter(Admin.id == id).one()
    return data

    






async def count_all_Admin():
    data = session.query(Admin).count()
    return data
