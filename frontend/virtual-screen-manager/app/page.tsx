"use client"

import React, { useState, useEffect } from 'react'
import { Button } from "../components/ui/button"
import { Input } from "../components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card"
import ScreenDisplay from '../components/ScreenDisplay'

const API_URL = 'http://127.0.0.1:5000'

interface Screen {
    id: string;
    name: string;
    content: string;
}

const borderColors = [
    'border-red-500',
    'border-blue-500',
    'border-green-500',
    'border-yellow-500',
    'border-purple-500',
    'border-pink-500',
    'border-indigo-500',
    'border-teal-500',
]

export default function VirtualScreenManager() {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [token, setToken] = useState('')
    const [screens, setScreens] = useState<Screen[]>([])
    const [error, setError] = useState('')

    useEffect(() => {
        if (token) {
            fetchScreens()
            // Set up interval to fetch screens every 2 seconds
            const intervalId = setInterval(fetchScreens, 2000)

            // Clean up interval on component unmount or when token changes
            return () => clearInterval(intervalId)
        }
    }, [token])

    const login = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
            const response = await fetch(`${API_URL}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            })
            if (!response.ok) throw new Error('Login failed')
            const data = await response.json()
            setToken(data.access_token)
            setError('')
        } catch (err) {
            setError('Login failed. Please check your credentials.')
        }
    }

    const fetchScreens = async () => {
        try {
            const response = await fetch(`${API_URL}/screens`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ token }),
            })
            if (!response.ok) throw new Error('Failed to fetch screens')
            const data = await response.json()
            setScreens(data)
        } catch (err) {
            setError('Failed to fetch screens')
        }
    }

    const updateScreen = async (screenId: string) => {
        const newContent = prompt('Enter new content for the screen:')
        if (newContent === null) return

        try {
            const response = await fetch(`${API_URL}/screens/content/update`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ token, screen_id: screenId, content: newContent }),
            })
            if (!response.ok) throw new Error('Failed to update screen content')
            alert('Screen content updated successfully')
            fetchScreens()
        } catch (err) {
            setError('Failed to update screen content')
        }
    }

    return (
        <div className="flex justify-center items-center min-h-screen bg-gray-900 p-4 text-gray-200">
            {!token ? (
                <Card className="w-full max-w-md bg-gray-800 border border-gray-700">
                    <CardHeader className="space-y-1">
                        <CardTitle className="text-2xl font-bold text-center text-white">Virtual Screen Manager</CardTitle>
                        <CardDescription className="text-center text-gray-400">Login to manage your virtual screens</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <form onSubmit={login} className="space-y-4">
                            <Input
                                type="text"
                                placeholder="Username"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                required
                                className="bg-gray-700 text-white border-gray-600"
                            />
                            <Input
                                type="password"
                                placeholder="Password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                                className="bg-gray-700 text-white border-gray-600"
                            />
                            <Button type="submit" className="w-full bg-blue-600 text-white hover:bg-blue-700">
                                Login
                            </Button>
                        </form>
                    </CardContent>
                </Card>
            ) : (
                <div className="w-full max-w-6xl">
                    <h1 className="text-3xl font-bold mb-6 text-center text-white">Your Virtual Screens</h1>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {screens.map((screen, index) => (
                            <ScreenDisplay 
                                key={screen.id} 
                                screen={screen} 
                                onUpdate={updateScreen}
                                borderColor={borderColors[index % borderColors.length]}
                            />
                        ))}
                    </div>
                </div>
            )}
            {error && <p className="text-red-400 mt-4 text-center absolute bottom-4 left-0 right-0">{error}</p>}
        </div>
    )
}