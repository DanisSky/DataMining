from graph_generator import create_graph
from matrix_generator import matrix_from_graph
from page_rank import page_rank
from services import get_page_links_v2

if __name__ == '__main__':
    URL = "https://makingfun.com/"

    d = get_page_links_v2(URL)

    create_graph(d)

    matrix, height, G_LIST = matrix_from_graph()

    page_rank(matrix, height, G_LIST)
