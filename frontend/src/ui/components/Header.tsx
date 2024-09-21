import { Logo } from "./Logo";
import { TabNavigation } from "./TabNavigation";

export function Header() {
	return (
		<header className="bg-neutral-100/50 backdrop-blur-md">
			<div className="mx-auto max-w-7xl px-3 sm:px-8">
				<div className="flex h-16 justify-between gap-5 md:gap-8">
					<Logo />
				</div>
			</div>
			<TabNavigation />
		</header>
	);
}
