"use client";

import { useEffect, useState } from "react";

interface User {
	id: number;
	name: string;
}

export default function UserList() {
	const [users, setUsers] = useState<User[]>([]);

	useEffect(() => {
		async function fetchUsers() {
			try {
				const response = await fetch("/api/users");
				if (!response.ok) {
					throw new Error("Failed to fetch users");
				}
				const data = await response.json();
				if (
					Array.isArray(data) &&
					data.every((item) => typeof item === "object" && "id" in item! && "name" in item)
				) {
					setUsers(data as User[]);
				} else {
					throw new Error("Invalid data format received");
				}
			} catch (error) {
				console.error("Error fetching users:", error);
				setUsers([]);
			}
		}
		fetchUsers();
	}, []);

	return (
		<div>
			<h1>Users</h1>
			<ul>
				{users.map((user) => (
					<li key={user.id}>{user.name}</li>
				))}
			</ul>
		</div>
	);
}
