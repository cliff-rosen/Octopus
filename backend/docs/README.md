# Virtual Screen Manager

## Project Overview

The Virtual Screen Manager is a web application that allows users and chatbots to collaboratively create, manage, and interact with "virtual screens." These virtual screens are web endpoints accessible via browsers and an API, enabling both users and chatbots to view and manipulate content to facilitate orchestration of multi-turn conversations that have complicated context graphs.

To use the system, two components are required:

1. A user account
2. A chatbot account with a system prompt that is programmed to interact with the virtual screens



## Key Features

1. User Authentication
2. Virtual Screen Management
3. Virtual Screen Interaction
4. API Integration for Chatbots
5. Dashboard Interface


## Basic Worklow
### Setup

1. User creates an with account and logs in
2. User c



4. User can register a device to access the virt

5. User can log out
## Backend API

The backend API is implemented using Flask and provides the following main endpoints:

- Authentication: `/auth/login`, `/auth/logout`
- Screen Management: `/screens`, `/screens/<screen_id>`
- Screen Interaction: `/api/screens/<screen_id>/read`, `/api/screens/<screen_id>/write`
- User Dashboard: `/user/dashboard`

## Current Implementation

The current implementation in `backend/application.py` includes:

- Basic user authentication with JWT
- CRUD operations for virtual screens
- API endpoints for reading and writing screen content
- A simple user dashboard

