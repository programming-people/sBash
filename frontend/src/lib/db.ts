import { Pool, type QueryResult } from "pg";

let pool!: Pool;

if (!pool) {
	pool = new Pool({
		connectionString: process.env.DATABASE_URL,
		ssl: {
			rejectUnauthorized: false,
		},
	});
}

interface QueryParams {
	query: string;
	values?: any[];
}

export async function executeQuery<T = any>({ query, values = [] }: QueryParams): Promise<QueryResult<T>> {
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
