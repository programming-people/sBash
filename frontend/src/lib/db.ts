import { Pool, QueryResult, QueryResultRow } from "pg";

let pool!: Pool;

// TypeScriptで環境変数からデータベースの接続URLを構築する
const dbUser = process.env.DB_USER || '';
const dbPass = process.env.DB_PASS || '';
const dbHost = process.env.DB_HOST || '';
const dbName = process.env.DB_NAME || '';

// 接続URLを構築
const connectionString = `postgresql://${dbUser}:${dbPass}@${dbHost}/${dbName}`;

if (!pool) {
	pool = new Pool({
		connectionString,
		ssl: {
			rejectUnauthorized: false,
		},
	});
}

interface QueryParams {
	query: string;
	values?: any[];
}

export async function executeQuery<T extends QueryResultRow = QueryResultRow>({ query, values = [] }: QueryParams): Promise<QueryResult<T>> {
	try {
		const client = await pool.connect();
		try {
			const result = await client.query(query, values);
			return result;
		} finally {
			client.release();
		}
	} catch (error) {
		console.error("Error executing query:", error);
		throw error;
	}
}
