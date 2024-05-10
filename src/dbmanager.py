import psycopg2


class DBManager:

    def __init__(self, dbname: str = 'postgres', user: str = 'postgres',
                 password: str = '569874b',
                 host: str = 'localhost', port: str = '5432'):
        self.conn = psycopg2.connect(dbname=dbname, user=user,
                                     password=password, host=host, port=port)
        self.cur = self.conn.cursor()

        self._create_tables()

    def _create_tables(self):
        with self.conn:
            self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS employers (
            employer_id INT PRIMARY KEY,
            accredited VARCHAR,
            employer_name VARCHAR NOT NULL,
            description TEXT,
            url VARCHAR NOT NULL,
            vacancies_url VARCHAR NOT NULL,
            area VARCHAR,
            industries VARCHAR
            );
            """)

        with self.conn:
            self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS vacancies (
            vacancy_id INT PRIMARY KEY,
            vacancy_name VARCHAR NOT NULL,
            salary_from INT, 
            salary_to INT, 
            employer_id INT REFERENCES employers(employer_id) NOT NULL, 
            currency VARCHAR,
            experience VARCHAR, 
            schedule VARCHAR, 
            employment VARCHAR, 
            requirement TEXT, 
            responsibility TEXT,
            professional_roles VARCHAR,
            url VARCHAR NOT NULL
            );
            """)

    def load_to_db(self, vacancies, companies):
        for company in companies:
            with self.conn:
                self.cur.execute(f"""INSERT INTO employers (employer_id,
                 accredited, employer_name, description, url, vacancies_url, 
                 area, industries) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
                returning *;""", company.to_list())
        for vacancy in vacancies:
            with self.conn:
                self.cur.execute(f"""INSERT INTO vacancies (vacancy_id, 
                vacancy_name, salary_from, salary_to, employer_id,
                currency, experience, schedule, employment, requirement, 
                responsibility, professional_roles, url) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                 returning *;""", vacancy.to_list())

    def get_companies_and_vacancies_count(self):
        with self.conn:
            self.cur.execute(f"""SELECT employer_name, COUNT(vacancy_id)
            FROM employers
            INNER JOIN vacancies USING(employer_id)
            GROUP BY employer_name;""")
            return self.cur.fetchall()

    def get_all_vacancies(self):
        with self.conn:
            self.cur.execute(f"""SELECT employer_name, vacancy_name, 
            salary_from, salary_to, currency, vacancies.url
            FROM vacancies
            INNER JOIN employers USING(employer_id);""")
            return self.cur.fetchall()

    def get_avg_salary(self):
        with self.conn:
            self.cur.execute(f"""SELECT(AVG(salary_from) + AVG(salary_to)) / 2 
            as average_salary
            FROM vacancies
            WHERE salary_from > 0 and salary_to > 0 and currency = 'руб.';""")
            return self.cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        with self.conn:
            self.cur.execute(f"""SELECT employer_name, vacancy_name, 
            salary_from, salary_to, currency, vacancies.url
            FROM vacancies
            INNER JOIN employers USING(employer_id)
            WHERE (salary_from + salary_to)/2 > 
            (SELECT(AVG(salary_from) + AVG(salary_to)) / 2 as average_salary
            FROM vacancies
            WHERE salary_from > 0 and salary_to > 0 and currency = 'руб.') 
            and currency = 'руб.'""")
            return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        with self.conn:
            self.cur.execute(f"""SELECT employer_name, vacancy_name, 
            salary_from, salary_to, currency, vacancies.url
            FROM vacancies
            INNER JOIN employers USING(employer_id)
            WHERE requirement LIKE '%{keyword}%' 
            and responsibility LIKE '%{keyword}%'""")
            return self.cur.fetchall()


if __name__ == '__main__':
    db = DBManager()
    print(db.get_vacancies_with_keyword('ython'))