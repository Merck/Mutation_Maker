/*   Copyright (c) 2020 Merck Sharp & Dohme Corp. a subsidiary of Merck & Co., Inc., Kenilworth, NJ, USA.
 *
 *   This file is part of the Mutation Maker, An Open Source Oligo Design Software For Mutagenesis and De Novo Gene Synthesis Experiments.
 *
 *   Mutation Maker is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation, either version 3 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

import * as R from 'ramda'
import {flattenMutations, Mutation, parseMutation} from '../genes'
import { notUndefined } from '../helpers'
import {
  PASResponseData, PASResultFragment,
  MSDMMutationData, MSDMResponseData,
  SSMResponseData
} from './Api'

// SSM
export type SSMResultData = SSMResponseData

export const responseToSSMResultData = (response: SSMResponseData): SSMResultData => response

// MSDM
const mutationDataToMSDMResultRecord = (mutationData: MSDMMutationData): MSDMResultRecord => ({
  mutations: flattenMutations(mutationData.mutations.map(parseMutation).filter(notUndefined)),
  result_found: mutationData.result_found,
  primers: mutationData.primers,
})

export const responseToMSDMResultData = (response: MSDMResponseData): MSDMResultData => ({
  results: response.results.map(mutationDataToMSDMResultRecord),
  full_sequence: response.full_sequence,
  goi_offset: response.goi_offset,
  input_data: response.input_data
})

export type MSDMResultRecord = {
  mutations: Mutation[]
  result_found: boolean
  primers: MSDMPrimer[]
}

export type MSDMResultDataInput = {
  config: any
}

export type MSDMResultData = {
  results: MSDMResultRecord[]
  full_sequence: string
  goi_offset: number,
  input_data: MSDMResultDataInput
}

export type MSDMPrimer = {
  sequence: string
  start: number
  length: number
  temperature: number
  gc_content: number
  degenerate_codons: string[]
  overlap_with_following?: boolean
}

export type MSDMFlatResultRecord = {
  mutations: Mutation[]
  result_found: boolean,
  ratio?: number
} & Partial<MSDMPrimer>

export type IndexedMSDMFlatResultRecord = MSDMFlatResultRecord & { index: number, ratio: number }

const resultRecordToFlatResultRecords = (resultRecord: MSDMResultRecord): MSDMFlatResultRecord[] =>
  R.isEmpty(resultRecord.primers)
    ? [
        {
          mutations: resultRecord.mutations,
          result_found: resultRecord.result_found,
        },
      ]
    : resultRecord.primers.map(primer => ({
        mutations: resultRecord.mutations,
        result_found: resultRecord.result_found,
        ...primer,
      }))

export const resultRecordsToFlatResultRecords = (
  resultRecords: MSDMResultRecord[],
): IndexedMSDMFlatResultRecord[] =>
  resultRecords
    .reduce((acc, record) => [...acc, ...resultRecordToFlatResultRecords(record)], [])
    .map((record, index) => ({ ...record, index, ratio: 0 }))


// PAS
export const resultRecordsToIndexedResultRecordsPas = (
  resultRecords: PASResultFragment[],
): IndexedPASResultFragment[] =>
  resultRecords
    .map((record, index) => ({ ...record, index }))

export const responseToPASResultData = (response: PASResponseData): PASResultData => ({
  results: response.results,
  input_data: response.input_data,
  full_sequence: response.full_sequence,
  goi_offset: response.goi_offset,
  message: response.message
})

export type PASResultData = {
  results: PASResultFragment[]
  input_data: PASResultDataInput
  full_sequence: string
  goi_offset: number
  message: string
}

export type PASResultDataInput = {
  sequences: any
  config: any
  mutations: any
  is_dna_sequence: boolean
  is_mutations_as_codons: boolean
}

export type IndexedPASResultFragment = PASResultFragment & { index: number }

export type PASPrimer = {
  sequence: string
  start: number
  length: number
  temperature: number
  gc_content: number
  degenerate_codons: string[]
}

export type PASFlatResultRecord = {
  mutations: Mutation[]
  length: number
  result_found: boolean
} & Partial<PASPrimer>

export type IndexedPASFlatResultRecord = PASFlatResultRecord & { index: number }
