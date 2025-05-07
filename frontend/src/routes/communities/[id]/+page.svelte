<script lang="ts">
    import Feed from '$components/Post/feed.svelte';
    import Annoucements from '$components/Post/annoucements.svelte';
    import Event from '$lib/components/Post/event.svelte';
    import { getUserInfo } from '$lib/api/checkUser';
    import type { MeResponse,communityData, response } from '$lib/api/apiType';
    import { get } from '$lib/api/get';
	import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import EditCommunityCard from "$components/communityCRUD/edit.svelte";
    import {checkPermisions,isWithCommunity} from '$lib/api/checkUser';
    import { post } from '$lib/api/post';
    import { deleteCall } from '$lib/api/delete';
    import Popup from '$components/ErrorPopUp/popup.svelte';

    let choice = 0;
	let userUrl = 'https://picsum.photos/id/63/200/200';
	let picture_url = '';
    let communityId: string;
    let modalShown = false;
    let hasPermission = false;
    let inCommunity = false;


	const tabs = [
        { label: 'Events'},
        { label: 'Announcements' },
    ];


    let author: MeResponse;
    let community: communityData;
    let communityFetched = false;
    let loggedin = false;
    let errorMessage = '';

    async function fetchUser() {
        try {
            const response = await getUserInfo();
            if (response && response.user) {
                author = response;
                loggedin = true;
            } else {
                throw new Error('Invalid user data');
            }
        } catch (error) {
            console.error('Error fetching user info:', error);
            loggedin = false;
        }
    }

    async function getCommunity() {
        try {
            let response:communityData = await get('community/'+communityId);
            console.log('Community response:', response);
            if (response.success) {
                community = response;
                communityFetched = true;
            }
        } catch (error) {
            console.error('Error fetching community:', error);
        }
    }


    async function joinCommunity() {
        try {
            const response:response = await post('community/'+communityId+'/members', {});
            if (response.success) {
                console.log('Joined community successfully');
                inCommunity = true;
            } else {
                console.error('Error joining community:', response.error_message);
                errorMessage = response.error_message[0];
            }
        } catch (error) {
            console.error('Error joining community:', error);
            errorMessage = 'Error joining community';
        }
    }

    async function leaveCommunity() {
        try {
            const response:response = await deleteCall('community/'+communityId+'/members', {});
            if (response.success) {
                console.log('left community successfully');
                inCommunity = false;
            } else {
                console.error('Error leaving community:', response.error_message);
                errorMessage = response.error_message[0];
            }
        } catch (error) {
            console.error('Error leaving community:', error);
            errorMessage = 'Error leaving community';
        }
    }



	onMount(async () => {
		if (localStorage.getItem('loggedin') === 'true') {
            communityFetched = false;
            errorMessage = '';
			try {
                communityId = $page.params.id;
                if (await checkPermisions(parseInt(communityId))) {
                    console.log('User has permissions to edit the community.');
                    hasPermission = true;
                } else {
                    console.log('User does not have permissions to edit the community.');
                    hasPermission = false;
                }

                if (await isWithCommunity(parseInt(communityId))) {
                    console.log('User is in the community.');
                    inCommunity = true;
                } else {
                    console.log('User is not in the community.');
                    inCommunity = false;
                }

                getCommunity();
				fetchUser();

			} catch (error) {
				console.error('Error parsing user info:', error);
			}
		}else {
            window.location.href = '/';
        }
	});

</script>


<EditCommunityCard bind:modalShown={modalShown} communityID={parseInt(communityId)} />



{#if loggedin}
    {#if author.user.picture_url != ''}
        <script>
            userUrl = author.user.picture_url;
            picture_url = author.user.picture_url;
        </script>
    {:else}
        <script>
            userUrl = 'https://picsum.photos/id/63/200/200';
            picture_url = 'https://picsum.photos/id/63/200/200';
        </script>
    {/if}
{/if}
<div class="flex flex-col h-screen">
    <Popup bind:errorMessage={errorMessage} />
    <div class="sticky top-0 bg-gray-300 z-50 shadow-md">
        <div class="flex flex-col items-center pt-5">
            {#if picture_url != ''}
                <a href={userUrl} target="_blank" rel="noopener noreferrer">
                    <img
                        src={picture_url}
                        alt="Profile Icon"
                        class="h-11 w-11 rounded-full border"
                    />
                </a>
            {/if}
            <h1 class="pt-5 text-center text-3xl font-bold">
                Welcome {loggedin && author?.user ? `${author.user.first_name} ${author.user.last_name}` : 'Guest'}
            </h1>
        </div>

        <div class="mt-4 flex justify-center border-b border-gray-300">
            {#each tabs as { label }, index}
                <button
                    class={`px-4 py-2 text-lg font-semibold ${
                        choice === index ? 'border-b-4 border-blue-500 text-blue-500' : 'text-gray-500'
                    }`}
                    on:click={() => (choice = index)}
                >
                    {label}
                </button>
            {/each}
        </div>
    </div>

    {#if loggedin}
    <div class="flex flex-1 overflow-hidden">
        <div class="w-1/4 p-4 hidden md:block">
            {#if loggedin}
                <div class="rounded-lg border-2 border-gray-300 bg-white p-4 shadow-md sticky top-5 mt-5">
                        <div
                        class="top-0 flex items-center space-x-2 rounded-t-2xl bg-white"
                    >
                        {#if author.user.picture_url != ''}
                            <a href={'url'} target="_blank" rel="noopener noreferrer">
                                <img src={author.user.picture_url} alt="Profile Icon" class="h-11 w-11 rounded-full" />
                            </a>
                        {:else}
                            <a href={'url'} target="_blank" rel="noopener noreferrer">
                                <img
                                    src="https://picsum.photos/id/63/200/200"
                                    alt="Profile Icon"
                                    class="h-11 w-11 rounded-full"
                                />
                            </a>
                        {/if}
                        <span class="font-bold">{author.user.first_name} {author.user.last_name}</span>
                        <a class="w-1/2 rounded bg-blue-500 px-4 py-2 text-white text-center block hover:bg-blue-600 ml-auto" href="/account">
                            Go To Profile
                        </a>
                    </div>
                </div>
            {/if}

            <div class="rounded-lg border-2 border-gray-300 bg-white p-4 shadow-md sticky top-5 mt-5">
                {#if communityFetched}
                    <h1 class="text-lg font-bold text-gray-700">
                        {community.name}
                    </h1>
                    <div class="mt-4 space-y-4">
                        <div class="rounded-lg border border-gray-300 bg-gray-100 p-4 hover:shadow-lg transition-shadow">
                            <p class="mt-1 text-sm text-gray-600">{community.description}</p>
                        </div>
                    </div>
                {/if}
                {#if inCommunity}
                    <button class="mt-4 w-full rounded bg-blue-500 px-4 py-2 text-white text-center block hover:bg-red-600" on:click={() => leaveCommunity()}>
                        Leave
                    </button>
                {:else}
                    <button class="mt-4 w-full rounded bg-blue-500 px-4 py-2 text-white text-center block hover:bg-green-600" on:click={() => joinCommunity()}>
                        Join
                    </button>
                {/if}
                {#if hasPermission}
                    <button class="mt-4 w-full rounded bg-blue-500 px-4 py-2 text-white text-center block hover:bg-blue-600" on:click={() => (modalShown = true)}>
                        Edit
                    </button>
                {/if}
            </div>

            <div class="rounded-lg border-2 border-gray-300 bg-white p-4 shadow-md sticky top-5 mt-5">
                {#if communityFetched}
                    <h1 class="text-lg font-bold text-gray-700">
                        Members
                    </h1>
                    <div class="mt-4 space-y-4">
                        <div class="rounded-lg border border-gray-300 bg-gray-100 p-4 hover:shadow-lg transition-shadow">
                            <p class="mt-1 text-sm text-gray-600">Jake</p>
                        </div>
                    </div>
                {/if}
            </div>
        </div>


        <div class="w-full md:w-1/2 px-4 overflow-y-auto scrollbar-none flex justify-center mt-2">
            <div class="w-full max-w-2xl">
                {#if choice === 0}
                    <div class="w-full">
                        <Feed feedType="events" showActions={true}>
                            <Event url={"community/"+communityId+"/events"} slot="Posts" limit={30} />
                        </Feed>
                    </div>
                {:else if choice === 1}
                    <div class="w-full">
                        <Feed feedType="announcements">
                            <Annoucements url={"community/"+communityId+"/announcements"} slot="Posts" limit={30} />
                        </Feed>
                    </div>
                {/if}
            </div>
        </div>

    </div>
    {/if}
</div>