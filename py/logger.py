# -*- coding: utf-8 -*-
import logging
from config import rootPath

logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.ERROR,
                    filename=rootPath + r'/log/running.err',
                    filemode='a',
                    )

logger = logging.getLogger(__name__)
