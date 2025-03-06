<script lang="ts">
	import Input from '$components/FormInput/Input.svelte';
	import Popup from '$components/ErrorPopUp/popup.svelte';
	import { post } from '$lib/Api/post';
	import type { response } from '$lib/Api/types';

	let email = '';
	let password = '';
	let errorMessage = '';



	async function handleLogin(event: Event) {
		event.preventDefault();
		let data = {
			email: email,
			password: password
		};
		let response =  await post('authorisation/login', data) as response;
		try {
			console.log(response);
			if (response.http_status === 201) {
				localStorage.setItem('loggedIn', 'true');
				alert('Login Successful');
				window.location.href = '/';
			} else if (response.http_status === 400) {
				if (response.error_message[0] === 'Invalid Email Or Password') {
					errorMessage = 'Invalid Email Or Password';
				} else if (response.error_message[0] === 'Email Not Verified') {
					errorMessage = 'Email Not Verified';
				} else {
					errorMessage = response.error_message.join(', ');
				}
			} else {
				errorMessage = 'An error occurred';
			}
		} catch (error) {
			errorMessage = 'An unexpected error occurred';
			console.error(error);
		}
	}

</script>

<h1>E:{errorMessage}</h1>

<div class="w-full p-8 md:w-1/2 md:mx-auto">
	<Popup bind:errorMessage />
	<h2 class="text-center text-2xl font-semibold text-gray-700">Login</h2>
	<p class="text-center text-xl text-gray-600">Welcome back!</p>
	<form on:submit|preventDefault={handleLogin}>
		<Input
			Name="Email"
			placeholder="Enter your email"
			type="email"
			showLabel={true}
			bind:value={email}
		/>
		<Input
			Name="Password"
			placeholder="Enter your password"
			type="password"
			showLabel={true}
			bind:value={password}
		/>
		<div
			class="mt-4 flex flex-col items-center justify-between space-y-2 md:flex-row md:space-y-0"
		>
			<button type="submit" class="rounded-lg bg-blue-600 px-6 py-2 text-white hover:bg-blue-900"
				>Login</button
			>
			<a href="/register" class="text-sm text-gray-600 hover:text-gray-900">Not got an Account?</a
			>
		</div>
	</form>
</div>