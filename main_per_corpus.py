from Core.GraphRAG import GraphRAG
from Option.Config2 import Config
import argparse
import os
import asyncio
from pathlib import Path
from shutil import copyfile
from Data.QueryDataset import RAGQueryDataset
import pandas as pd
from Core.Utils.Evaluation import Evaluator
from Core.Common.Logger import logger


def check_dirs(opt):
    """Create necessary directories for results, configs, and metrics"""
    # For each query, save the results in a separate directory
    result_dir = os.path.join(opt.working_dir, opt.exp_name, "Results")
    # Save the current used config in a separate directory
    config_dir = os.path.join(opt.working_dir, opt.exp_name, "Configs")
    # Save the metrics of entire experiment in a separate directory
    metric_dir = os.path.join(opt.working_dir, opt.exp_name, "Metrics")
    os.makedirs(result_dir, exist_ok=True)
    os.makedirs(config_dir, exist_ok=True)
    os.makedirs(metric_dir, exist_ok=True)
    opt_name = args.opt[args.opt.rindex("/") + 1 :]
    basic_name = os.path.join(args.opt.split("/")[0], "Config2.yaml")
    copyfile(args.opt, os.path.join(config_dir, opt_name))
    copyfile(basic_name, os.path.join(config_dir, "Config2.yaml"))
    return result_dir, metric_dir


async def process_corpus_sample(corpus_item, questions, opt, corpus_idx, result_dir):
    """
    Process a single corpus sample: build graph, query questions, and save results
    
    Args:
        corpus_item: Single corpus document
        questions: List of questions for this corpus
        opt: Configuration object
        corpus_idx: Index of the corpus sample
        result_dir: Directory to save results
    
    Returns:
        List of results for this corpus sample
    """
    logger.info(f"\n{'='*80}")
    logger.info(f"Processing corpus sample {corpus_idx}: {corpus_item.get('title', 'Untitled')}")
    logger.info(f"Number of questions for this corpus: {len(questions)}")
    logger.info(f"{'='*80}\n")
    
    # Create a unique index name for this corpus sample
    original_index_name = opt.index_name
    opt.index_name = f"{original_index_name}_corpus_{corpus_idx}"
    
    # Initialize GraphRAG instance for this corpus sample
    digimon = GraphRAG(config=opt)
    
    # Build graph for this single corpus sample
    logger.info(f"Building graph for corpus {corpus_idx}...")
    await digimon.insert([corpus_item])
    
    # Query all questions for this corpus sample
    logger.info(f"Querying {len(questions)} questions for corpus {corpus_idx}...")
    corpus_results = []
    for q_idx, query in enumerate(questions):
        logger.info(f"  Question {q_idx + 1}/{len(questions)}: {query['question'][:100]}...")
        res = await digimon.query(query["question"])
        query["output"] = res
        query["corpus_id"] = corpus_idx
        query["corpus_title"] = corpus_item.get("title", "")
        corpus_results.append(query)
    
    # Save results for this corpus sample
    corpus_result_path = os.path.join(result_dir, f"corpus_{corpus_idx}_results.json")
    corpus_results_df = pd.DataFrame(corpus_results)
    corpus_results_df.to_json(corpus_result_path, orient="records", lines=True)
    logger.info(f"Saved results for corpus {corpus_idx} to {corpus_result_path}")
    
    # Restore original index name
    opt.index_name = original_index_name
    
    return corpus_results


async def process_all_corpus_samples(query_dataset, opt, result_dir):
    """
    Process all corpus samples in the dataset
    
    Args:
        query_dataset: RAGQueryDataset instance
        opt: Configuration object
        result_dir: Directory to save results
    
    Returns:
        Path to the combined results file
    """
    corpus_list = query_dataset.get_corpus()
    all_results = []
    
    logger.info(f"Total corpus samples to process: {len(corpus_list)}")
    
    for corpus_idx in range(len(corpus_list)):
        corpus_item = corpus_list[corpus_idx]
        
        # Get questions for this corpus sample
        questions = query_dataset.get_questions_for_corpus(corpus_idx)
        
        if len(questions) == 0:
            logger.warning(f"No questions found for corpus {corpus_idx}, skipping...")
            continue
        
        # Process this corpus sample
        corpus_results = await process_corpus_sample(
            corpus_item, questions, opt, corpus_idx, result_dir
        )
        all_results.extend(corpus_results)
    
    # Save combined results
    combined_path = os.path.join(result_dir, "all_results.json")
    all_results_df = pd.DataFrame(all_results)
    all_results_df.to_json(combined_path, orient="records", lines=True)
    logger.info(f"\nSaved combined results to {combined_path}")
    logger.info(f"Total questions processed: {len(all_results)}")
    
    return combined_path


async def wrapper_evaluation(path, opt, metric_dir):
    """Evaluate the results"""
    eval = Evaluator(path, opt.dataset_name)
    res_dict = await eval.evaluate()
    save_path = os.path.join(metric_dir, "metrics.json")
    with open(save_path, "w") as f:
        f.write(str(res_dict))
    logger.info(f"Saved evaluation metrics to {save_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-opt", type=str, help="Path to option YMAL file.")
    parser.add_argument("-dataset_name", type=str, help="Name of the dataset.")
    args = parser.parse_args()

    opt = Config.parse(Path(args.opt), dataset_name=args.dataset_name)
    result_dir, metric_dir = check_dirs(opt)

    query_dataset = RAGQueryDataset(
        data_dir=os.path.join(opt.data_root, opt.dataset_name)
    )

    # Process all corpus samples
    save_path = asyncio.run(process_all_corpus_samples(query_dataset, opt, result_dir))

    # Evaluate results
    asyncio.run(wrapper_evaluation(save_path, opt, metric_dir))

    logger.info("\n" + "="*80)
    logger.info("Processing complete!")
    logger.info("="*80)
