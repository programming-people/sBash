"use client";

import { useState } from "react";

const tabs = ["マインドマップ", "サービス"];

export function TabNavigation() {
	const [activeTab, setActiveTab] = useState("マインドマップ");

	const renderContent = () => {
		switch (activeTab) {
			case "マインドマップ":
				return <div>Welcome to our homepage!</div>;
			case "サービス":
				return <div>Here are our products.</div>;
			default:
				return null;
		}
	};

	return (
		<>
			<nav className="bg-gray-800">
				<div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
					<div className="flex h-12 items-center justify-start">
						<div className="flex space-x-4">
							{tabs.map((tab) => (
								<button
									key={tab}
									onClick={() => setActiveTab(tab)}
									className={`rounded-md px-3 py-2 text-sm font-medium ${
										activeTab === tab
											? "bg-gray-900 text-white"
											: "text-gray-300 hover:bg-gray-700 hover:text-white"
									}`}
								>
									{tab}
								</button>
							))}
						</div>
					</div>
				</div>
			</nav>
			<div className="mx-auto mt-4 max-w-7xl px-4 sm:px-6 lg:px-8">{renderContent()}</div>
		</>
	);
}
