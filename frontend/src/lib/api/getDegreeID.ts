import type { PaginationDataResponse } from '$lib/api/apiType';
import { get } from '$lib/api/get';

export async function getDegreeID(name: string) {
    const response = (await get('degrees/list/?name=' + name)) as PaginationDataResponse;
    if (response.success === true) {
        console.log('Degree ID fetched successfully');
        return response.degrees[0].id;
    } else {
        console.error('Error fetching tag ID:', response.error_message);
        return -1;
    }
}

export async function getDegreeName(id: string) {
    const response = (await get('degrees/?id=' + id)) as PaginationDataResponse;
    if (response.success === true) {
        console.log('Tag Name fetched successfully');
        return response.degree.name;
    } else {
        console.error('Error fetching tag Name:', response.error_message);
        return "";
    }
}
