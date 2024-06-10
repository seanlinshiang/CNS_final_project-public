import argparse
import json
from llm_utils import LLM
from progressbar import progressbar
import os
import time

def load_dataset(file_dir):

    with open(file_dir, 'r') as file:
        data = json.load(file)

    return data


def main(args):
    llm = LLM(args.model, args.temperature)
    dataset = load_dataset(args.dataset_path)

    for ds in progressbar(dataset, redirect_stdout=True):
        context = ds['context']
        print(f'id: {ds["id"]}: {context[:64]}...')
        response = llm.get_response(context)
        print(f'response: {response[:64]}...')
        ds['response'] = response
        time.sleep(3.0)

    _, filename = os.path.split(args.dataset_path)
    output_file_name = os.path.join(args.output_dir, f"{filename.split('.')[0]}_response.json")
    print(f'Output file: {output_file_name}')

    with open(output_file_name, 'w') as output_file:
        json.dump(dataset, output_file)
    
    print(f'Finished')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', required=True)
    parser.add_argument('-d', '--dataset_path', required=True)
    parser.add_argument('--output_dir', default='responses')
    parser.add_argument('--temperature', default=0.9)

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    main(args)