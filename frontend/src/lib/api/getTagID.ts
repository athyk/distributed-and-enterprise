import type { PaginationDataResponse } from '$lib/api/apiType';
import { get } from '$lib/api/get';


export async function getTagID(name: string) {
    let response = (await get('tags/list/?name=' + name)) as PaginationDataResponse;
    if (response.success === true) {
        console.log('Tag ID fetched successfully');
        return response.tags[0].id;
    } else {
        console.error('Error fetching tag ID:', response.error_message);
        return -1;
    }
}