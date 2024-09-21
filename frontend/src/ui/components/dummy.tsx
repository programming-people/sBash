import React from 'react';
import { ProductList } from './ProductList';

interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  currency: string;
  image: string;
}

const dummyProducts: Product[] = [
  {
    id: '1',
    name: 'スマートフォン X',
    description: '最新のハイエンドスマートフォン',
    price: 99999,
    currency: 'JPY',
    image: 'https://example.com/smartphone-x.jpg',
  },
  {
    id: '2',
    name: 'ラップトップ Pro',
    description: 'プロフェッショナル向け高性能ラップトップ',
    price: 199999,
    currency: 'JPY',
    image: 'https://example.com/laptop-pro.jpg',
  },
  {
    id: '3',
    name: 'ワイヤレスイヤホン Y',
    description: 'ノイズキャンセリング機能付きワイヤレスイヤホン',
    price: 29999,
    currency: 'JPY',
    image: 'https://example.com/wireless-earphones-y.jpg',
  },
  {
    id: '4',
    name: 'スマートウォッチ Z',
    description: '健康管理機能搭載のスマートウォッチ',
    price: 39999,
    currency: 'JPY',
    image: 'https://example.com/smartwatch-z.jpg',
  },
  {
    id: '5',
    name: 'タブレット A',
    description: '軽量で持ち運びに便利なタブレット',
    price: 49999,
    currency: 'JPY',
    image: 'https://example.com/tablet-a.jpg',
  },
];

export default function Dummy() {
  return (
    <div>
      <ProductList products={dummyProducts} />
    </div>
  );
}