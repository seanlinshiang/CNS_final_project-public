import json
import os

'''
Load dataset from file_dir
json structure: 
{
    "contexts": [
        ...
    ],
    "injection_prompts: [
        ...
    ]
}
'''
def load_base_dataset(file_dir):

    with open(file_dir, 'r') as file:
        data = json.load(file)

    contexts = data['contexts']
    injection_prompts = data['injection_prompts']

    return contexts, injection_prompts


'''
Perform prompt injection to context
e.g.
inj_prompt: xxxx
context: "Science !@top@! is the systematic pursuit !@middle@!of knowledge through observation!@bottom@!."
position: top

return: "Science xxxx is the systematic pursuit of knowledge through observation."
'''
def inject_context(inj_prompt, context, position):
    unused_position = ["top", "middle", "bottom"]
    unused_position.remove(position)

    try:
        for pos in ["top", "middle", "bottom"]:
            assert context.count(f'!@{pos}@!') == 1, f"Multiple {pos}: {context}"
    except AssertionError as err:
        print(err)

    injection_placement = f'!@{position}@!'
    injected_context = context.replace(injection_placement, inj_prompt)

    # Remove unused injection placements
    for pos in unused_position:
        inj_place = f'!@{pos}@!'
        injected_context = injected_context.replace(inj_place, '')
    
    return injected_context


'''
Generate dataset
data format:
{
    "id": x, 
    "context": xxxx,
    "length": x,
    "system_prompt": xxxx,
    "injection_prompt": xxxx,
    "attack_target": xxxx,
    "attack_mode": xxxx,
    "position": xxxx
}
'''
def generate_from_base(base_dataset, attack_target):
    contexts, injection_prompts = base_dataset

    dataset = []
    ip_len = len(injection_prompts)
    for context_index, context_obj in enumerate(contexts):

        for ip_ind, ip_obj in enumerate(injection_prompts):
            index = context_index * ip_len + ip_ind

            context = context_obj['system_prompt'] + context_obj['user_prompt']
            injected_context = inject_context(
                ip_obj['injection_prompt'], 
                context,
                ip_obj['position']
            )

            new_data = {
                "id": index, 
                "context": injected_context,
                "length": context_obj['length'],
                "system_prompt": context_obj['system_prompt'],
                "injection_prompt": ip_obj['injection_prompt'],
                "attack_target": attack_target,
                "attack_id": ip_obj['attack_id'],
                "position": ip_obj['position']
            }
            
            dataset.append(new_data)

    return dataset

if __name__ == '__main__':
    attack_targets = []
    for file in os.listdir('base_datasets'):
        if file.endswith('.json'):
            attack_targets.append(file.split('.')[0])

    print(f'Generating...')
    for attack_target in attack_targets:
        print(f"base_datasets/{attack_target}.json => datasets/{attack_target}_dataset.json")
        base_dataset = load_base_dataset(os.path.join('base_datasets', f'{attack_target}.json'))
        ds = generate_from_base(base_dataset, attack_target)

        output_file_name = os.path.join("datasets", f"{attack_target}_dataset.json")
        with open(output_file_name, 'w') as output_file:
            json.dump(ds, output_file)