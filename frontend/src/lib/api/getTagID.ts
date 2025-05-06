import type { PaginationDataResponse,PaginationData } from '$lib/api/apiType';
import { get } from '$lib/api/get';

export async function getTagID(name: string) {
	const response = (await get('tags/list/?name=' + name)) as PaginationDataResponse;
	if (response.success === true) {
		console.log('Tag ID fetched successfully');
		return response.tags[0].id;
	} else {
		console.error('Error fetching tag ID:', response.error_message);
		return -1;
	}
}

export async function getTagName(id: string) {
	const response = (await get('tags/?id=' + id)) as PaginationDataResponse;
	if (response.success === true) {
		console.log('Tag Name fetched successfully');
		return response.tag.name;
	} else {
		console.error('Error fetching tag Name:', response.error_message);
		return -1;
	}
}
