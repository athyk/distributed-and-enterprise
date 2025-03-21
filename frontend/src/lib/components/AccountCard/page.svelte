<script lang="ts">
	import Input from '$components/FormInput/Input.svelte';
	import SearchBox from '$components/SearchBox/searchBox.svelte';

	export let email: string[] | undefined = undefined;
	export let password: string[] | undefined = undefined;
	export let password_comfirm = false;

	export let first_name: string[] | undefined = undefined;
	export let last_name: string[] | undefined = undefined;
	export let dob: string[] | undefined = undefined;

	export let gender: [string, string, string[]] | undefined = undefined;

	export let degree: [[string, number][], string, string] | undefined = undefined;
	export let year_of_study: [number, number, string] | undefined = undefined;
	export let graduation_date: [number, string] | undefined = undefined;

	export let tags: [[string, number][], string, string] | undefined = undefined;

	export let password_comfirm_value: string | undefined = undefined;

	export let otp: [string, string, string] | undefined = undefined;

	let current_year = new Date().getFullYear();
	let max_grad_year = current_year + 5;
</script>

{#if email}
	{#if email[1] !== ''}
		<label for={email[1]} class="block text-gray-700">{email[1]} </label>
	{/if}
	<input
		type="email"
		{...email[1] !== '' ? { placeholder: email[2] } : {}}
		{...email[1] !== '' ? { id: email[1] } : {}}
		bind:value={email[0]}
		class="mt-2 mb-2 w-full rounded-md border px-4 py-2 focus:ring-1 focus:ring-blue-600 focus:outline-none"
	/>
{/if}

{#if password}
	<label for={password[1]} class="block text-gray-700">{password[1]} </label>
	<input
		type="password"
		{...password[1] !== '' ? { placeholder: password[2] } : {}}
		{...password[1] !== '' ? { id: password[1] } : {}}
		bind:value={password[0]}
		class="mt-2 mb-2 w-full rounded-md border px-4 py-2 focus:ring-1 focus:ring-blue-600 focus:outline-none"
	/>

	{#if password_comfirm}
		{#if password[1] !== ''}
			<label for={password[1]} class="block text-gray-700">{password[1]} </label>
		{/if}
		<input
			type="password"
			bind:value={password_comfirm_value}
			placeholder="Confirm Password"
			id="password"
			class="mt-2 mb-2 w-full rounded-md border px-4 py-2 focus:ring-1 focus:ring-blue-600 focus:outline-none"
		/>
	{/if}
{/if}

{#if first_name}
	<Input
		Name={first_name[1]}
		placeholder={first_name[2]}
		type="text"
		showLabel={first_name[1] !== ''}
		required={true}
		bind:value={first_name[0]}
	/>
{/if}

{#if last_name}
	<Input
		Name={last_name[1]}
		placeholder={last_name[2]}
		type="text"
		showLabel={last_name[1] !== ''}
		required={true}
		bind:value={last_name[0]}
	/>
{/if}

{#if dob}
	<Input
		Name={dob[1]}
		placeholder={dob[2]}
		type="date"
		showLabel={dob[1] !== ''}
		required={true}
		bind:value={dob[0]}
	/>
{/if}

{#if gender}
	<div class="mt-4">
		<label for="gender" class="block text-gray-700">
			{gender[1]}
		</label>
		<div>
			{#each gender[2] as g}
				<input
					type="radio"
					name="gender"
					id={`gender-${g}`}
					value={g}
					class="py mt-2 rounded-md border px-4"
					bind:group={gender[0]}
				/>
				<label class="mr-5" for={`gender-${g}`}>{g}</label>
			{/each}
		</div>
	</div>
{/if}

{#if tags}
	<SearchBox
		Name={tags[2]}
		showLabel={tags[2] !== ''}
		url={tags[1]}
		id={tags[0]}
		multi_select={true}
		max_select={5}
		bind:selected={tags[0]}
	/>
{/if}

{#if degree}
	<SearchBox
		Name={degree[2]}
		showLabel={degree[2] !== ''}
		url={degree[1]}
		id={degree[0]}
		bind:selected={degree[0]}
	/>
{/if}

{#if year_of_study}
	<div class="mt-4">
		<label for="year_of_study" class="block text-gray-700">
			{year_of_study[2]}
		</label>
		<div class="mt-2 flex items-center">
			<div class=" rounded px-5 py-1 text-black">
				<span>{year_of_study[0]}</span>
			</div>
			<input
				type="range"
				id="year_of_study"
				min="1"
				max="5"
				step="1"
				bind:value={year_of_study[0]}
				class="ml-4 w-1/2"
			/>
		</div>
	</div>
{/if}

{#if graduation_date}
	<div class="mt-4">
		<label for="year_of_study" class="block text-gray-700">
			{graduation_date[1]}
		</label>
		<div class="mt-2 flex items-center">
			<div class=" rounded px-2 py-1 text-black">
				<span>{graduation_date[0]}</span>
			</div>
			<input
				type="range"
				id="year_of_study"
				min={current_year}
				max={max_grad_year}
				step="1"
				bind:value={graduation_date[0]}
				class="ml-4 w-1/2"
			/>
		</div>
	</div>
{/if}

{#if otp}
	{#if otp[1] !== ''}
		<label for={otp[1]} class="block text-gray-700">{otp[1]} </label>
	{/if}
	<input
		type="text"
		{...otp[1] !== '' ? { placeholder: otp[2] } : {}}
		{...otp[1] !== '' ? { id: otp[1] } : {}}
		bind:value={otp[0]}
		class="mt-2 mb-2 w-full rounded-md border px-4 py-2 focus:ring-1 focus:ring-blue-600 focus:outline-none"
	/>
{/if}
