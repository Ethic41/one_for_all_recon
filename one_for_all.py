#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2022-01-06 22:20:00
# @Author  : Dahir Muhammad Dahir
# @Description : something cool


import os
from typing import List

from threading import Thread
from helpers import get_line_separated_file_content_from_input
from Sublist3r import sublist3r # type: ignore
from pwn import process # type: ignore


def main():
    print("""
    ############################################################
    #           ooOoOOOo One_For_All_Recon oOOOoOoo            #
    #                =====[   Author   ]=====                  #
    #       ooooOoOOOo Dahir Muhammad Dahir oOOOoOoooo         #
    ############################################################
    """)

    recon_single_program()


def recon_single_program():
    program_name = input("Enter the bug bounty program name: ").strip()
    create_program_directory(program_name)
    number_of_threads = int(input("Enter the number of threads [default is 10]: ").strip())
    number_of_threads = number_of_threads if number_of_threads else 10
    scope_subdomains = get_single_program_scope()
    sublister_subdomains = sublister_recon(scope_subdomains, threads=number_of_threads)
    valid_subdomains = verify_subdomains(sublister_subdomains)

    write_to_file(f"output_files/{program_name}/resolved_subdomains", valid_subdomains)
    write_to_file(f"output_files/{program_name}/unresolved_subdomains", set(sublister_subdomains) - valid_subdomains)


def get_single_program_scope():
    return get_line_separated_file_content_from_input(
        "Enter the program scope file path, [Enter] to use default (sample_files/single_program_scope.dmd)",
        default_file_path="sample_files/single_program_scope.dmd",
    )


def sublister_recon(
    domains,
    threads=10,
    savefile=None,
    ports=None,
    silent=False,
    verbose=True,
    enable_bruteforce=False,
    engine=None
) -> List[str]:
    output_subdomains: List[str] = []

    for domain in domains:
        subdomains = sublist3r.main(domain, threads=threads, savefile=savefile, ports=ports, silent=silent, \
            verbose=verbose, enable_bruteforce=enable_bruteforce, engines=engine,)
        output_subdomains.extend(subdomains)
    
    return output_subdomains


def verify_subdomains(subdomains, max_threads=10):
    valid_subdomains = set()
    
    def dig_subdomain(subdomain):
        ps = process(["dig", "+short", subdomain, ";", "exit"])
        output = ps.recvall().decode().split()
        if output and output[0]:
            valid_subdomains.add(subdomain)

    def create_workers(jobs: List[str]):
        workers: List[Thread] = []

        for job in jobs:
            worker = Thread(target=dig_subdomain, args=(job,))
            workers.append(worker)
        
        for worker in workers:
            worker.start()
        
        for worker in workers:
            worker.join()
        
        print(f"Completed verifying {current_round * len(jobs)} subdomains out of {subdomains_count} subdomains")


    subdomains_count = len(subdomains)
    total_rounds = subdomains_count // max_threads if subdomains_count % max_threads == 0 else \
        subdomains_count // max_threads + 1
    current_round = 0

    if subdomains_count <= max_threads:
        current_round = 1
        create_workers(subdomains)
    else:
        for i in range(total_rounds):
            current_round += 1
            create_workers(subdomains[i * max_threads: (i + 1) * max_threads])

    return valid_subdomains


def create_program_directory(name):
    if os.path.isdir(f"output_files/{name}"):
        pass
    else:
        os.mkdir(f"output_files/{name}")


def write_to_file(filename, subdomains):
    with open(filename, "w") as f:
        for subdomain in subdomains:
            f.write(f"{subdomain}\n")

if __name__ == "__main__":
    main()

