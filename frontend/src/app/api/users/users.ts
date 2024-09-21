import { NextResponse } from 'next/server';
import { executeQuery } from '@/lib/db'; // データベース接続用のユーティリティ

interface User {
  id: number;
  name: string;
}

export async function GET() {
  try {
    const result = await executeQuery<User>({
      query: 'SELECT * FROM users',
    });

    // データベースクエリの結果を取得
    const users = result.rows;

    // 成功レスポンスを返す
    return NextResponse.json(users, { status: 200 });
  } catch (error) {
    console.error('Error fetching users:', error);
    // エラーレスポンスを返す
    return NextResponse.json(
      { error: 'Failed to fetch users' },
      { status: 500 }
    );
  }
}