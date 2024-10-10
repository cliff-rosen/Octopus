from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

# API Documentation

"""
Authentication Endpoints:

POST /auth/login
    Authenticate a user and return a session token.
    Request body: {"username": string, "password": string}
    Response: {"access_token": string} or {"msg": "Invalid credentials"}

POST /auth/logout
    Invalidate the current session token.
    Requires JWT authentication.
    Response: {"msg": "Logout successful"}

Virtual Screen Management Endpoints:

GET /screens
    Retrieve a list of virtual screens for the authenticated user.
    Requires JWT authentication.
    Response: List of screen objects

POST /screens
    Create a new virtual screen.
    Requires JWT authentication.
    Response: Newly created screen object

GET /screens/<screen_id>
    Retrieve details of a specific virtual screen.
    Requires JWT authentication.
    Response: Screen object or {"msg": "Screen not found or access denied"}

PUT /screens/<screen_id>
    Update a specific virtual screen.
    Requires JWT authentication.
    Response: Updated screen object or {"msg": "Screen not found or access denied"}

DELETE /screens/<screen_id>
    Delete a specific virtual screen.
    Requires JWT authentication.
    Response: {"msg": "Screen deleted"} or {"msg": "Screen not found or access denied"}
"""
