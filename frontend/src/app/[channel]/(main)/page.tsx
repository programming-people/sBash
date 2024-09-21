import { ProductListByCollectionDocument } from "@/gql/graphql";
import { executeGraphQL } from "@/lib/graphql";
import Dummy from "@/ui/components/Dummy";
// import { ProductList } from "@/ui/components/ProductList";

export const metadata = {
	title: "みんつく : みんなで作るアイディアやサービス",
	description:
		"みんつくでアイディアやサービスを発表してアイディアを肉付けしたり、サービスの開発を始めてみよう！",
};

// interface User {
// 	id: number;
// 	name: string;
// }

export default async function Page({ params }: { params: { channel: string } }) {
	const data = await executeGraphQL(ProductListByCollectionDocument, {
		variables: {
			slug: "featured-products",
			channel: params.channel,
		},
		revalidate: 60,
	});

	if (!data.collection?.products) {
		return null;
	}

	// const products = data.collection?.products.edges.map(({ node: product }) => product);

	return (
		<section className="mx-auto max-w-7xl p-8 pb-16">
			<h2 className="sr-only">Product list</h2>
			<Dummy />
		</section>
	);
}
