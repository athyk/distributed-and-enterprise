<script lang="ts">
    import Feed from '$components/Post/feed.svelte';
    import Post from '$components/Post/post.svelte';
    import Annoucements from '$components/Post/annoucements.svelte';
    import Event from '$lib/components/Post/event.svelte';

	import { onMount } from 'svelte';

    let choice = 0;
	let name = '';
	let userUrl = 'https://picsum.photos/id/63/200/200';
	let picture_url = '';

	const tabs = [
        { label: 'Posts', component: Post, feedType: 'posts', url: 'posts/list' },
        { label: 'Events', component: Event, feedType: 'events', url: 'community/events', showActions: true },
        { label: 'Announcements', component: Annoucements, feedType: 'announcements', url: 'community/announcements' }
    ];

	const communities = [
		{ name: 'Community 1', description: 'Description Text Here' , member_count: 10},
		{ name: 'Community 2', description: 'Another description here.' , member_count: 5},
		{ name: 'Community 3', description: 'Yet another description.' , member_count: 20},
	];

	const recent_Posts = [
		{ name: 'Post 1', created_at: '1742949086', description: 'Description Text Here' },
		{ name: 'Post 2', created_at: '1742949086', description: 'Another description here.' },
		{ name: 'Post 3', created_at: '1742949086', description: 'Yet another description.' },
	]

	//localhost:8000/community/search?offset=0&limit=10&is_with=1
	//localhost:8000/posts/list?user_id=1&offset=0&limit=5


	onMount(() => {
		if (localStorage.getItem('loggedin') === 'true') {
			const userInfo = localStorage.getItem('userInfo');
			try {
				let user = JSON.parse(userInfo).user;
				name = user.first_name+' ' + user.last_name;
				picture_url = user.picture_url;
				userUrl = '/user/' + user.id.toString();
			} catch (error) {
				console.error('Error parsing user info:', error);
				name = 'Guest';
			}
		} else {
			name = 'Guest';
		}
	});

</script>


<div class="flex flex-col h-screen">
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
            <h1 class="pt-5 text-center text-3xl font-bold">Welcome {name}</h1>
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


    <div class="flex flex-1 overflow-hidden">
        <div class="w-1/4 p-4 hidden md:block">
            <div class="rounded-lg border-2 border-gray-300 bg-white p-4 shadow-md sticky top-5">
                <h1 class="text-lg font-bold text-gray-700">Unlock the full potential of UniHub</h1>
                <ul class="mt-2 space-y-2 list-disc list-inside text-gray-600">
                    <li>Communicate with fellow Students</li>
                    <li>Find out about the latest news</li>
                    <li>Join events and activities</li>
                </ul>
                <a class="mt-4 w-full rounded bg-blue-500 px-4 py-2 text-white text-center block" href="/register">
                    Create an account
                </a>
				<p class="mt-2 text-center text-sm text-gray-500">
					Already have an account? <a href="/login" class="text-blue-500">Login</a>
				</p>
            </div>

			<div class="rounded-lg border-2 border-gray-300 bg-white p-4 shadow-md sticky top-5 mt-5">
				<h1 class="text-lg font-bold text-gray-700">My Recent Posts</h1>
				<div class="mt-4 space-y-4">
					{#each recent_Posts as post}
						<div class="rounded-lg border border-gray-300 bg-gray-100 p-4 hover:shadow-lg transition-shadow">
							<h2 class="text-gray-800 font-semibold ">{post.name}</h2>
							<p class="mt-1 text-sm text-gray-600">{post.description}</p>
						</div>
					{/each}
				</div>
				<a class="mt-4 w-full rounded bg-blue-500 px-4 py-2 text-white text-center block hover:bg-blue-600" href="/communities">
					View All
				</a>
			</div>
        </div>


        <div class="w-full md:w-1/2 px-4 overflow-y-auto scrollbar-none flex justify-center mt-2">
            <div class="w-full max-w-2xl">
                {#if choice === 0}
                    <div class="w-full">
                        <Feed feedType="posts">
                            <Post url="posts/list" slot="Posts" limit={30} />
                        </Feed>
                    </div>
                {:else if choice === 1}
                    <div class="w-full">
                        <Feed feedType="events" showActions={true} communityID={1}>
                            <Event url="community/events" slot="Posts" limit={30} />
                        </Feed>
                    </div>
                {:else if choice === 2}
                    <div class="w-full">
                        <Feed feedType="announcements">
                            <Annoucements url="community/announcements" slot="Posts" limit={30} />
                        </Feed>
                    </div>
                {/if}
            </div>
        </div>

		<div class="w-1/4 p-4 hidden md:block">
			<div class="rounded-lg border-2 border-gray-300 bg-white p-4 shadow-md sticky top-5">
				<h1 class="text-lg font-bold text-gray-700">My Top Communities</h1>
				<div class="mt-4 space-y-4">
					{#each communities as community}
						<div class="rounded-lg border border-gray-300 bg-gray-100 p-4 hover:shadow-lg transition-shadow">
							<h2 class="text-gray-800 font-semibold ">{community.name}</h2>
							<p class="mt-1 text-sm text-gray-600">{community.member_count} members</p>
							<p class="mt-1 text-sm text-gray-600">{community.description}</p>
							<a class="mt-2 text-blue-500 hover:underline" href="/community/{community.name}">
								Go to
							</a>
						</div>
					{/each}
				</div>
				<a class="mt-4 w-full rounded bg-blue-500 px-4 py-2 text-white text-center block hover:bg-blue-600" href="/communities">
					Find More
				</a>
			</div>
		</div>
    </div>
</div>