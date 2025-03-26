const base_url = 'http://localhost:8000/';
export async function Put<T>(url: string, data: Record<string, unknown>, formData?: FormData): Promise<T> {
	try {
		const response = await fetch(base_url + url, {
			method: 'PUT',
			headers: formData ? undefined : { 'Content-Type': 'application/json' },
			body: formData || JSON.stringify(data),
			credentials: 'include'
		});

		const responseData = await response.json();

		if (!response.ok) {
			return responseData as T;
		}

		return responseData as T;
	} catch (error) {
		throw new Error('Failed to fetch: ' + error);
	}
}
