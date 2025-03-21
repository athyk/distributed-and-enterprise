const base_url = 'http://localhost:8000/';
export async function post<T>(url: string, data: Record<string, unknown>): Promise<T> {
	try {
		const response = await fetch(base_url + url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		});

		const responseData = await response.json();

		if (!response.ok) {
			return responseData as T;
		}

		return responseData as T;
	} catch (error) {
		throw new Error('Failed to fetch' + error);
	}
}
