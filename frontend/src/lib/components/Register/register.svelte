<script lang="ts">
	import Input from '$lib/components/FormInputButton/Input.svelte';

	let email = '';
	let password = '';
	let passwordConfirm = '';

	let fName = '';
	let lName = '';
	let dob = '';
	let gender = '';

	let degree = '';
	let degreeYear = '';
	let graduationYear = '';

	let tags = '';

	function handleSubmit() {
		console.log('Email:', email);
		console.log('Password:', password);
	}

	let step = 1;
	let maxstep = 3;
</script>

<div
	class="mx-auto mt-5 flex h-[50vh] w-1/2 overflow-hidden rounded-lg border-1 border-black bg-white shadow-lg"
>
	<div
		class="hidde</div>n w-1/2 bg-cover md:block"
		style="background-image: url('https://images.unsplash.com/photo-1521587760476-6c12a4b040da?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')"
	></div>
	<div class="w-full p-8 md:w-1/2">
		<h2 class="text-center text-2xl font-semibold text-gray-700">Register</h2>
		<p class="text-center text-xl text-gray-600">Fill in User Info</p>
		<form on:submit|preventDefault={handleSubmit}>
			{#if step === 1}
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
				<Input
					Name="Confirm Password"
					placeholder="Confirm your password"
					type="password"
					showLabel={true}
					bind:value={passwordConfirm}
				/>
			{/if}

			{#if step === 2}
				<Input
					Name="First Name"
					placeholder="Enter your first name"
					type="text"
					showLabel={true}
					bind:value={fName}
				/>
				<Input
					Name="Last Name"
					placeholder="Enter your last name"
					type="text"
					showLabel={true}
					bind:value={lName}
				/>
				<Input
					Name="Date of Birth"
					placeholder="Enter your date of birth"
					type="date"
					showLabel={true}
					bind:value={dob}
				/>
				<Input
					Name="Gender"
					placeholder="Enter your Gender"
					type="text"
					showLabel={true}
					bind:value={gender}
				/>
			{/if}

			{#if step === 3}
				<Input
					Name="Degree"
					placeholder="Enter your degree"
					type="text"
					showLabel={true}
					bind:value={degree}
				/>
				<Input
					Name="Degree Year"
					placeholder="Enter your degree year"
					type="number"
					showLabel={true}
					bind:value={degreeYear}
				/>
				<Input
					Name="Graduation Year"
					placeholder="Enter your graduation year"
					type="number"
					showLabel={true}
					bind:value={graduationYear}
				/>
				<Input
					Name="Tags"
					placeholder="Enter your tags"
					type="text"
					showLabel={true}
					bind:value={tags}
				/>
			{/if}

			<div
				class="mt-4 flex flex-col items-center justify-between space-y-2 md:flex-row md:space-y-0"
			>
				<button
					type="button"
					class="rounded-lg bg-blue-600 px-6 py-2 text-white hover:bg-blue-900"
					on:click={() => (step = Math.min(maxstep, step + 1))}
				>
					Next Step
				</button>
				{#if step === 1}
					<a href="/login" class="text-sm text-gray-600 hover:text-gray-900"
						>Already have an Account?</a
					>
				{/if}
			</div>
		</form>
	</div>
</div>
