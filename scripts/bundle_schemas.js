#!/usr/bin/env node
/**
 * Bundle Beacon v2 JSON schemas for Pydantic model generation.
 *
 * Strategy:
 * - Entity models: Copy pre-dereferenced schemas from beacon-v2/bin/deref_schemas/
 * - Framework schemas: Bundle using json-schema-ref-parser (these resolve correctly)
 *
 * Usage:
 *   npm install @apidevtools/json-schema-ref-parser
 *   node scripts/bundle_schemas.js
 */

const $RefParser = require('@apidevtools/json-schema-ref-parser');
const fs = require('fs');
const path = require('path');

// Configuration
// BEACON_V2_ROOT can be overridden via environment variable
const BEACON_V2_ROOT = process.env.BEACON_V2_ROOT
  ? path.resolve(process.env.BEACON_V2_ROOT)
  : path.resolve(__dirname, '../tmp/beacon-v2-schemas');
const OUTPUT_DIR = path.resolve(__dirname, '../tmp/bundled_schemas');

const FRAMEWORK_DIR = path.join(BEACON_V2_ROOT, 'framework', 'json');
const DEREF_SCHEMAS_DIR = path.join(BEACON_V2_ROOT, 'bin', 'deref_schemas');

// Pre-dereferenced entity schemas (just copy these)
const ENTITY_SCHEMAS = {
  'individual': path.join(DEREF_SCHEMAS_DIR, 'individuals', 'defaultSchema.json'),
  'biosample': path.join(DEREF_SCHEMAS_DIR, 'biosamples', 'defaultSchema.json'),
  'cohort': path.join(DEREF_SCHEMAS_DIR, 'cohorts', 'defaultSchema.json'),
  'dataset': path.join(DEREF_SCHEMAS_DIR, 'datasets', 'defaultSchema.json'),
  'run': path.join(DEREF_SCHEMAS_DIR, 'runs', 'defaultSchema.json'),
  'analysis': path.join(DEREF_SCHEMAS_DIR, 'analyses', 'defaultSchema.json'),
  'genomicVariation': path.join(DEREF_SCHEMAS_DIR, 'genomicVariations', 'defaultSchema.json'),
};

// Framework schemas (need bundling)
const FRAMEWORK_SCHEMAS = {
  // Common
  'common': path.join(FRAMEWORK_DIR, 'common', 'beaconCommonComponents.json'),
  'ontologyTerm': path.join(FRAMEWORK_DIR, 'common', 'ontologyTerm.json'),

  // Requests
  'requestBody': path.join(FRAMEWORK_DIR, 'requests', 'beaconRequestBody.json'),
  'requestMeta': path.join(FRAMEWORK_DIR, 'requests', 'beaconRequestMeta.json'),
  'filteringTerms': path.join(FRAMEWORK_DIR, 'requests', 'filteringTerms.json'),

  // Responses
  'booleanResponse': path.join(FRAMEWORK_DIR, 'responses', 'beaconBooleanResponse.json'),
  'countResponse': path.join(FRAMEWORK_DIR, 'responses', 'beaconCountResponse.json'),
  'resultsetsResponse': path.join(FRAMEWORK_DIR, 'responses', 'beaconResultsetsResponse.json'),
  'collectionsResponse': path.join(FRAMEWORK_DIR, 'responses', 'beaconCollectionsResponse.json'),
  'infoResponse': path.join(FRAMEWORK_DIR, 'responses', 'beaconInfoResponse.json'),
  'errorResponse': path.join(FRAMEWORK_DIR, 'responses', 'beaconErrorResponse.json'),
  'filteringTermsResponse': path.join(FRAMEWORK_DIR, 'responses', 'beaconFilteringTermsResponse.json'),
  'mapResponse': path.join(FRAMEWORK_DIR, 'responses', 'beaconMapResponse.json'),

  // Response Sections
  'responseMeta': path.join(FRAMEWORK_DIR, 'responses', 'sections', 'beaconResponseMeta.json'),
  'resultsets': path.join(FRAMEWORK_DIR, 'responses', 'sections', 'beaconResultsets.json'),
};

/**
 * Copy a pre-dereferenced schema file
 */
function copySchema(name, sourcePath) {
  console.log(`Copying ${name}...`);

  if (!fs.existsSync(sourcePath)) {
    console.warn(`  WARNING: Schema file not found: ${sourcePath}`);
    return false;
  }

  const outputPath = path.join(OUTPUT_DIR, `${name}.json`);
  fs.copyFileSync(sourcePath, outputPath);

  const stats = fs.statSync(outputPath);
  console.log(`  -> ${outputPath} (${(stats.size / 1024).toFixed(1)} KB)`);
  return true;
}

/**
 * Bundle a framework schema using json-schema-ref-parser
 */
async function bundleSchema(name, schemaPath) {
  console.log(`Bundling ${name}...`);

  if (!fs.existsSync(schemaPath)) {
    console.warn(`  WARNING: Schema file not found: ${schemaPath}`);
    return false;
  }

  try {
    const schema = await $RefParser.dereference(schemaPath, {
      dereference: {
        circular: 'ignore'
      }
    });

    const outputPath = path.join(OUTPUT_DIR, `${name}.json`);
    fs.writeFileSync(outputPath, JSON.stringify(schema, null, 2));

    const stats = fs.statSync(outputPath);
    console.log(`  -> ${outputPath} (${(stats.size / 1024).toFixed(1)} KB)`);
    return true;
  } catch (error) {
    console.error(`  ERROR bundling ${name}: ${error.message}`);
    return false;
  }
}

async function main() {
  console.log('Beacon v2 Schema Bundler');
  console.log('========================\n');
  console.log(`Beacon v2 root: ${BEACON_V2_ROOT}`);
  console.log(`Output directory: ${OUTPUT_DIR}\n`);

  // Check beacon-v2 exists
  if (!fs.existsSync(BEACON_V2_ROOT)) {
    console.error(`ERROR: Beacon v2 directory not found: ${BEACON_V2_ROOT}`);
    process.exit(1);
  }

  // Check deref_schemas exists
  if (!fs.existsSync(DEREF_SCHEMAS_DIR)) {
    console.error(`ERROR: Pre-dereferenced schemas not found: ${DEREF_SCHEMAS_DIR}`);
    console.error('Make sure your beacon-v2 clone includes the bin/deref_schemas directory.');
    process.exit(1);
  }

  // Create output directory
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  let successful = 0;
  let failed = 0;

  // Copy pre-dereferenced entity schemas
  console.log('--- Entity Schemas (pre-dereferenced) ---\n');
  for (const [name, schemaPath] of Object.entries(ENTITY_SCHEMAS)) {
    if (copySchema(name, schemaPath)) {
      successful++;
    } else {
      failed++;
    }
  }

  // Bundle framework schemas
  console.log('\n--- Framework Schemas (bundling) ---\n');
  for (const [name, schemaPath] of Object.entries(FRAMEWORK_SCHEMAS)) {
    if (await bundleSchema(name, schemaPath)) {
      successful++;
    } else {
      failed++;
    }
  }

  // Summary
  console.log('\n========================');
  console.log('Summary:');
  console.log(`  Successful: ${successful}`);
  console.log(`  Failed: ${failed}`);
  console.log(`\nBundled schemas written to: ${OUTPUT_DIR}`);
  console.log('\nNext step: Run the Python model generator:');
  console.log('  uv run python scripts/generate_from_bundled.py');

  process.exit(failed > 0 ? 1 : 0);
}

main().catch(console.error);
