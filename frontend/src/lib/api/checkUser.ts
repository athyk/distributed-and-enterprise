import { get } from './get';
import type { MeResponse, response } from './apiType';

export async function getUserInfo(): Promise<MeResponse> {
	const response = (await get('users/@me')) as MeResponse;
	if (response.success) {
		return response;
	} else {
		return response;
	}
}

export async function isLoggedIn(): Promise<boolean> {
	const response = await getUserInfo();
	if (response.success) {
		return true;
	} else {
		return false;
	}
}

export async function isUserID(userId: number,useLocalStorage=false): Promise<boolean> {
	if(useLocalStorage){
		const userInfoString = localStorage.getItem('userInfo');
		if (userInfoString) {
			const userInfo = JSON.parse(userInfoString) as MeResponse;
			return userInfo.user.id === userId;
		}
	}
	const response = await getUserInfo();
	if (response.success) {
		return response.user.id === userId;
	} else {
		return false;
	}
}

export async function checkPermisions(communityId:number): Promise<boolean> {
	const response = await get(`community/${communityId}/members`) as response;
	let msg = response.error_message[0].toUpperCase();
	if (msg === 'USER ROLE: ADMIN' || msg === 'USER ROLE: MODERATOR') {
		return true;
	}else{
		return false;
	}
}