import csv
import io
import apache_beam as beam

from apache_beam.options.pipeline_options import (
    PipelineOptions,
    GoogleCloudOptions
)


class ValidateClaim(beam.DoFn):

    VALID_STATUSES = {
        "APPROVED",
        "PENDING",
        "REJECTED"
    }

    def process(self, line):

        try:
            row = next(csv.DictReader(io.StringIO(line)))

            claim_id = row["claim_id"]
            member_id = row["member_id"]
            provider_id = row["provider_id"]
            claim_amount = row["claim_amount"]
            claim_status = row["claim_status"]

            # -------------------------------
            # Validation rules
            # -------------------------------

            if not claim_id:
                raise ValueError("Missing claim_id")

            if not member_id:
                raise ValueError("Missing member_id")

            if not provider_id:
                raise ValueError("Missing provider_id")

            if not claim_amount:
                raise ValueError("Missing claim_amount")

            # Must be numeric
            amount = float(claim_amount)

            if amount < 0:
                raise ValueError("Negative claim_amount")

            if claim_status not in self.VALID_STATUSES:
                raise ValueError(
                    f"Invalid claim_status: {claim_status}"
                )

            # -------------------------------
            # Standardized record
            # -------------------------------

            standardized = (
                f"{claim_id},"
                f"{member_id},"
                f"{provider_id},"
                f"{row['service_date']},"
                f"{amount:.2f},"
                f"{claim_status}"
            )

            yield beam.pvalue.TaggedOutput(
                "valid",
                standardized
            )

        except Exception as e:

            quarantine_record = (
                f"{line},"
                f"ERROR={str(e)}"
            )

            yield beam.pvalue.TaggedOutput(
                "invalid",
                quarantine_record
            )


def run():

    project_id = "YOUR_PROJECT_ID"
    bucket = "YOUR_BUCKET"

    input_file = (
        f"gs://{bucket}/"
        "raw/claims/"
        "ingestion_date=2026-08-21/"
        "claims.csv"
    )

    standardized_output = (
        f"gs://{bucket}/"
        "standardized/claims/claims"
    )

    quarantine_output = (
        f"gs://{bucket}/"
        "quarantine/claims/claims"
    )

    options = PipelineOptions(
        runner="DataflowRunner",
        project=project_id,
        region="asia-south1",
        staging_location=f"gs://{bucket}/dataflow/staging",
        temp_location=f"gs://{bucket}/dataflow/temp",
        job_name="healthcare-claims-validation"
    )

    with beam.Pipeline(options=options) as pipeline:

        results = (
            pipeline
            | "Read Claims File"
            >> beam.io.ReadFromText(
                input_file,
                skip_header_lines=1
            )
            | "Validate Claims"
            >> beam.ParDo(
                ValidateClaim()
            ).with_outputs(
                "valid",
                "invalid"
            )
        )

        (
            results.valid
            | "Write Valid Claims"
            >> beam.io.WriteToText(
                standardized_output,
                file_name_suffix=".csv"
            )
        )

        (
            results.invalid
            | "Write Invalid Claims"
            >> beam.io.WriteToText(
                quarantine_output,
                file_name_suffix=".csv"
            )
        )


if __name__ == "__main__":
    run()
