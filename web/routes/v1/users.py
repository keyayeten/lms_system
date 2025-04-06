from robyn import SubRouter, jsonify, Request

from core.db import get_session
from services.users import create_user, get_user, get_all_users, delete_user


users = SubRouter(__file__, prefix="/users")


@users.post("/")
async def create_user_route(request: Request):
    data = request.json()
    name = data.get("name")
    email = data.get("email")

    async for session in get_session():
        user = await create_user(session, name, email)
        return jsonify({"id": user.id, "name": user.name, "email": user.email})


@users.get("/")
async def list_users(request):
    async for session in get_session():
        users = await get_all_users(session)
        return jsonify([
            {"id": u.id, "name": u.name, "email": u.email} for u in users
        ])


@users.get("/:id")
async def get_user_route(request):
    user_id = int(request.path_params["id"])
    async for session in get_session():
        user = await get_user(session, user_id)
        if user:
            return jsonify({"id": user.id, "name": user.name, "email": user.email})
        return {"error": "User not found"}, 404


@users.delete("/:id")
async def delete_user_route(request):
    user_id = int(request.path_params["id"])
    async for session in get_session():
        success = await delete_user(session, user_id)
        if success:
            return {"message": "User deleted"}
        return {"error": "User not found"}, 404
