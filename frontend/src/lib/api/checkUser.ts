import { get } from "./get";
import type {MeResponse} from "./apiType";

export async function getUserInfo(): Promise<MeResponse> {
    let response = await get('users/@me') as MeResponse;
    if (response.success) {
        return response;
    } else {
        return response;
    }
}

export async function isLoggedIn(): Promise<boolean> {
    let response = await getUserInfo();
    if (response.success) {
        return true;
    } else {
        return false;
    }
}

export async function isUserID(userId: number): Promise<boolean> {
    let response = await getUserInfo();
    if (response.success) {
        return response.user.id === userId;
    } else {
        return false;
    }
}