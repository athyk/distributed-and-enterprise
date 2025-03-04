<script lang="ts">
	let email = '';
	let password = '';

	import Input from '$components/FormInput/Input.svelte';

	function handleLogin() {
		console.log('Email:', email);
		console.log('Password:', password);
	}
</script>


<div class="w-full p-8 md:w-1/2 md:mx-auto">
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