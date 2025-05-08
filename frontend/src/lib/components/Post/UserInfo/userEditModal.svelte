<script lang="ts">
	import CreateEditBase from '../CreateEdit/base.svelte';
	import SearchBox from '$components/SearchBox/searchBox.svelte';
	import type { MeResponse, response } from '$lib/api/apiType';
	import { onMount } from 'svelte';
	import { getDegreeName } from '$lib/api/getDegreeID';
	import { getTagName } from '$lib/api/getTagID';
	import { Put } from '$lib/api/Put';
	import { post } from '$lib/api/post.ts';
	import Popup from '$components/ErrorPopUp/popup.svelte';
	import type { ImageUploadResponse } from '$lib/api/apiType';

	export let modalShown = false;
	export let userInfo: MeResponse;
	export let refreshKey = 0;

	let tags: [string, number][] = [];
	let degree: [string, number][] = [];
	let images = [] as string[];

	let first_name: string;
	let last_name: string;
	let email: string;
	let date_of_birth: string;
	let year_of_study: number;
	let password: string;
	let confirm_password: string;
	let errorMessage: string;
	let gender: string;
	let image_success = false;

	function hideModal() {
		modalShown = false;
		refreshKey += 1;
	}

	async function fileSelected(event: Event) {
		if (!event.target || !(event.target as HTMLInputElement).files) {
			console.error('No file selected');
			return;
		}

		const file = (event.target as HTMLInputElement).files?.[0];
		if (!file) {
			console.error('No file selected');
			return;
		}
		const formData = new FormData();
		formData.append('file', file);

		try {
			let imageResponse = (await post('users/@me/profile', {}, formData)) as ImageUploadResponse;
			if (imageResponse.success === true) {
				console.log('Image uploaded successfully');
				images = [...images, imageResponse.file_url];
				console.log(images);
				image_success = true;
			} else {
				console.error('Error uploading image:', imageResponse.error);
			}
		} catch (error) {
			console.error('Error uploading image:', error);
		}
	}

	async function Submit() {
		console.log('Submit clicked');
		if (password && password !== confirm_password) {
			errorMessage = 'Passwords do not match';
			return;
		}

		let data = {
			user: {
				email,
				first_name,
				last_name,
				date_of_birth: date_of_birth ? date_of_birth.split('-').reverse().join('-') : '',
				year_of_study,
				degree_id: degree.length > 0 ? degree[0][1] : null,
				tags: tags.map((tag) => tag[1]),
				grad_date: userInfo.user.grad_date
			},
			password: password,
			new_password: password,
			otp: '',
			skip_email: true
		};
		let response = (await Put('users/@me', data)) as response;
		if (response.success === true) {
			console.log('User Info Updated Successfully');
			hideModal();
		} else {
			console.error('Error updating user info:', response.error_message);
		}
	}

	async function getTags() {
		if (userInfo.user.tags) {
			userInfo.user.tags.forEach(async (tag) => {
				const tagName = await getTagName(tag.toString());
				tags.push([tagName, tag]);
			});
		}
	}

	async function fetchDegreeName() {
		if (userInfo.user.degree_id) {
			try {
				const degreeName = await getDegreeName(userInfo.user.degree_id.toString());
				// Create a new array assignment instead of using push
				degree = [[degreeName, userInfo.user.degree_id]];
				console.log('Degree set to:', degree);
			} catch (error) {
				console.error('Error fetching degree name:', error);
			}
		}
	}

	onMount(async () => {
		errorMessage = '';
		first_name = userInfo.user.first_name;
		last_name = userInfo.user.last_name;
		email = userInfo.user.email;
		date_of_birth = userInfo.user.date_of_birth;
		year_of_study = userInfo.user.year_of_study;
		password = '';
		confirm_password = '';
		image_success = false;
		gender = userInfo.user.gender
			? userInfo.user.gender.charAt(0).toUpperCase() + userInfo.user.gender.slice(1)
			: '';
		getTags();
		fetchDegreeName();
		console.log('User Info:', userInfo);
		console.log('Tags:', tags);
		console.log('Degree:', degree);
	});
</script>

{#if modalShown}
	<div
		class="bg-gray bg-opacity-75 fixed inset-0 z-50 flex items-center justify-center p-4 backdrop-blur-sm"
	>
		<CreateEditBase
			ModalTitle={'Edit Account'}
			onSubmit={Submit}
			onClose={hideModal}
			ButtonText={'Save'}
		>
			<svelte:fragment slot="content">
				<div class="flex gap-2">
					<div class="flex w-full flex-col">
						<label for="first_name" class="mb-1 text-sm font-semibold">First Name</label>
						<input
							id="first_name"
							bind:value={first_name}
							placeholder="First Name"
							class="w-full rounded-lg border-2 border-gray-300 p-2 focus:border-blue-500 focus:outline-none"
						/>
					</div>
					<div class="flex w-full flex-col">
						<label for="last_name" class="mb-1 text-sm font-semibold">Last Name</label>
						<input
							id="last_name"
							bind:value={last_name}
							placeholder="Last Name"
							class="w-full rounded-lg border-2 border-gray-300 p-2 focus:border-blue-500 focus:outline-none"
						/>
					</div>
				</div>
				<div class="mt-2 flex w-full flex-col">
					<label for="date_of_birth" class="mb-1 text-sm font-semibold">Date of Birth</label>
					<input
						id="date_of_birth"
						bind:value={date_of_birth}
						type="date"
						class="w-full rounded-lg border-2 border-gray-300 p-2 focus:border-blue-500 focus:outline-none"
					/>
				</div>
				<div class="mt-2 flex w-full flex-col">
					<label for="gender" class="mb-1 text-sm font-semibold">Gender</label>
					<select
						id="gender"
						bind:value={gender}
						class="w-full rounded-lg border-2 border-gray-300 p-2 focus:border-blue-500 focus:outline-none"
					>
						<option value="" disabled>Select Gender</option>
						<option value="Male">Male</option>
						<option value="Female">Female</option>
						<option value="Other">Other</option>
					</select>
				</div>
				<div class="mt-2 flex w-full flex-col">
					<label for="degree" class="mb-1 text-sm font-semibold">Degree</label>
					<SearchBox
						classStyle="w-full border-2 border-gray-300 rounded-lg p-2 mt-2 focus:outline-none focus:border-blue-500"
						marginTop=""
						placeholder="Search for Degree..."
						url="degrees/list/"
						id="degree"
						multi_select={false}
						bind:selected={degree}
					/>
				</div>
				<div class="mt-2 flex w-full flex-col">
					<label for="year_of_study" class="mb-1 text-sm font-semibold">Year of Study</label>
					<input
						id="year_of_study"
						bind:value={year_of_study}
						type="number"
						min="1"
						max="7"
						class="w-full rounded-lg border-2 border-gray-300 p-2 focus:border-blue-500 focus:outline-none"
					/>
				</div>
				<div class="mt-2 flex w-full flex-col">
					<label for="tags" class="mb-1 text-sm font-semibold">Tags</label>
					<SearchBox
						classStyle="w-full border-2 border-gray-300 rounded-lg p-2 mt-2 focus:outline-none focus:border-blue-500"
						marginTop=""
						placeholder="Search for Tags..."
						url="tags/list/"
						id="tags"
						multi_select={true}
						max_select={5}
						bind:selected={tags}
					/>
				</div>
				<div class="mt-2 flex w-full flex-col">
					<label for="new_password" class="mb-1 text-sm font-semibold">New Password</label>
					<input
						id="new_password"
						bind:value={password}
						type="password"
						placeholder="New Password"
						class="w-full rounded-lg border-2 border-gray-300 p-2 focus:border-blue-500 focus:outline-none"
					/>
				</div>
				<div class="mt-2 flex w-full flex-col">
					<label for="confirm_password" class="mb-1 text-sm font-semibold">Confirm Password</label>
					<input
						id="confirm_password"
						bind:value={confirm_password}
						type="password"
						placeholder="Confirm Password"
						class="w-full rounded-lg border-2 border-gray-300 p-2 focus:border-blue-500 focus:outline-none"
					/>
				</div>
			</svelte:fragment>
			<svelte:fragment slot="actions">
				<input
					type="file"
					accept="image/*"
					id={'fileInput'}
					class="hidden"
					on:change={fileSelected}
				/>
				<button
					class="{image_success
						? 'bg-green-500 hover:bg-green-500'
						: 'bg-yellow-500 hover:bg-yellow-600'} rounded px-4 py-2 text-white"
					on:click={() => document.getElementById('fileInput')?.click()}
					disabled={image_success}
				>
					{image_success ? 'Image Updated' : 'Change Profile Image'}
				</button>
			</svelte:fragment>
		</CreateEditBase>
		<Popup bind:errorMessage />
	</div>
{/if}
