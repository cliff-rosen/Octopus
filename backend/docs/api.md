# Backend API Specification

## Authentication

### POST /auth/login
Authenticate a user and return a session token.

### POST /auth/logout
Invalidate the current session token.

### POST /auth/refresh
Refresh an existing session token.

## Virtual Screen Management

### GET /screens
Retrieve a list of virtual screens for the authenticated user.

### POST /screens
Create a new virtual screen.

### GET /screens/{screenId}
Retrieve details of a specific virtual screen.

### PUT /screens/{screenId}
Update a specific virtual screen.

### DELETE /screens/{screenId}
Delete a specific virtual screen.

## Virtual Screen Interaction

### GET /screens/{screenId}/content
Retrieve the current content of a virtual screen.

### POST /screens/{screenId}/content
Update the content of a virtual screen.

### GET /screens/{screenId}/status
Get the current status of a virtual screen.

## API Integration for Chatbots

### POST /api/screens/{screenId}/read
Allow chatbots to read content from a specific virtual screen.

### POST /api/screens/{screenId}/write
Allow chatbots to write content to a specific virtual screen.

## User Dashboard

### GET /user/dashboard
Retrieve dashboard information for the authenticated user.

### GET /user/screens/status
Get the status of all virtual screens for the authenticated user.

## Multi-Device Access

### POST /screens/{screenId}/devices
Register a new device for a specific virtual screen.

### DELETE /screens/{screenId}/devices/{deviceId}
Unregister a device from a specific virtual screen.

### GET /screens/{screenId}/devices
List all devices connected to a specific virtual screen.

