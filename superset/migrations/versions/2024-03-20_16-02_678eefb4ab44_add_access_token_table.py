# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Add access token table

Revision ID: 678eefb4ab44
Revises: be1b217cd8cd
Create Date: 2024-03-20 16:02:58.515915

"""

# revision identifiers, used by Alembic.
revision = "678eefb4ab44"
down_revision = "be1b217cd8cd"

import sqlalchemy as sa  # noqa: E402
from alembic import op  # noqa: E402
from sqlalchemy_utils import EncryptedType  # noqa: E402


def upgrade():
    op.create_table(
        "database_user_oauth2_tokens",
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("changed_on", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("database_id", sa.Integer(), nullable=False),
        sa.Column(
            "access_token",
            EncryptedType(),
            nullable=True,
        ),
        sa.Column("access_token_expiration", sa.DateTime(), nullable=True),
        sa.Column(
            "refresh_token",
            EncryptedType(),
            nullable=True,
        ),
        sa.Column("created_by_fk", sa.Integer(), nullable=True),
        sa.Column("changed_by_fk", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["changed_by_fk"],
            ["ab_user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["created_by_fk"],
            ["ab_user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["database_id"],
            ["dbs.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["ab_user.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_user_id_database_id",
        "database_user_oauth2_tokens",
        ["user_id", "database_id"],
    )


def downgrade():
    # get all foreign keys for table database_user_oauth2_tokens
    connection = op.get_bind()
    inspector = sa.engine.reflection.Inspector.from_engine(connection)
    foreign_keys = inspector.get_foreign_keys("database_user_oauth2_tokens")

    # drop all foreign keys
    for fk in foreign_keys:
        op.drop_constraint(
            fk["name"], "database_user_oauth2_tokens", type_="foreignkey"
        )

    op.drop_index("idx_user_id_database_id", table_name="database_user_oauth2_tokens")
    op.drop_table("database_user_oauth2_tokens")
