import React from 'react';
import { ProductList } from './ProductList';

interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  currency: string;
  image: string;
  slug: string;
}

const dummyProducts: Product[] = [
  {
    id: '1',
    name: 'マインドマップ１',
    description: '最新のハイエンドスマートフォン',
    price: 99999,
    currency: 'JPY',
    image: 'https://example.com/smartphone-x.jpg',
    slug: 'smartphone-x', // {{ edit_2 }} Added slug value
  },
  {
    id: '2',
    name: 'マインドマップ２',
    description: 'プロフェッショナル向け高性能ラップトップ',
    price: 199999,
    currency: 'JPY',
    image: 'https://example.com/laptop-pro.jpg',
    slug: 'laptop-pro', // {{ edit_3 }} Added slug value
  },
  {
    id: '3',
    name: 'マインドマップ３',
    description: 'ノイズキャンセリング機能付きワイヤレスイヤホン',
    price: 29999,
    currency: 'JPY',
    image: 'https://example.com/wireless-earphones-y.jpg',
    slug: 'wireless-earphones-y', // {{ edit_4 }} Added slug value
  },
  {
    id: '4',
    name: 'マインドマップ４',
    description: '健康管理機能搭載のスマートウォッチ',
    price: 39999,
    currency: 'JPY',
    image: 'https://example.com/smartwatch-z.jpg',
    slug: 'smartwatch-z', // {{ edit_5 }} Added slug value
  },
  {
    id: '5',
    name: 'マインドマップ５',
    description: '軽量で持ち運びに便利なタブレット',
    price: 49999,
    currency: 'JPY',
    image: 'https://example.com/tablet-a.jpg',
    slug: 'tablet-a', // {{ edit_6 }} Added slug value
  },
];

export default function DummyIdea() {
  return (
    <div>
      <ProductList products={dummyProducts} />
    </div>
  );
}