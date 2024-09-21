import Link from "next/link";

const footerLinks = [
	{
		title: "マインドマップ",
		links: [
			{ name: "探す", href: "/mindmap/search" },
			{ name: "作る", href: "/mindmap/create" },
		],
	},
	{
		title: "サービス",
		links: [
			{ name: "探す", href: "/services/search" },
			{ name: "作る", href: "/services/create" },
		],
	},
	{
		title: "サポート",
		links: [
			{ name: "FAQ", href: "/faq" },
			{ name: "お問い合わせ", href: "/contact" },
		],
	},
];

export function Footer() {
	const currentYear = new Date().getFullYear();

	return (
		<footer className="border-neutral-300 bg-neutral-50">
			<div className="mx-auto max-w-7xl px-4 lg:px-8">
				<div className="grid grid-cols-1 gap-8 py-16 md:grid-cols-3">
					{footerLinks.map((section) => (
						<div key={section.title}>
							<h3 className="text-sm font-semibold text-neutral-900">{section.title}</h3>
							<ul className="mt-4 space-y-4">
								{section.links.map((link) => (
									<li key={link.name} className="text-sm">
										<Link href={link.href} className="text-neutral-500 hover:text-neutral-600">
											{link.name}
										</Link>
									</li>
								))}
							</ul>
						</div>
					))}
				</div>
				<div className="flex flex-col justify-between border-t border-neutral-200 py-10 sm:flex-row">
					<p className="text-sm text-neutral-500">Copyright &copy; {currentYear} みんつく.</p>
				</div>
			</div>
		</footer>
	);
}
